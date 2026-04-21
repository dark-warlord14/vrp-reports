# use-after-free in Serial

| Field | Value |
|-------|-------|
| **Issue ID** | [40060298](https://issues.chromium.org/issues/40060298) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Serial, Platform>Apps>API>Serial |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2022-07-15 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**  

Will attach details soon.

**Problem Description:**  

.

**Additional Comments:**

\*\*Chrome version: \*\* 105.0.5178.0 \*\*Channel: \*\* Stable

**OS:** Windows

## Attachments

- [background.js](attachments/background.js) (text/plain, 86 B)
- [manifest.json](attachments/manifest.json) (text/plain, 263 B)

## Timeline

### he...@gmail.com (2022-07-15)

When the mojo method |GetDevices| (or |OpenPort|) [1] of interface |SerialPortManager| is called, there exists the following call chain (if the feature `enable-bluetooth-spp-in-serial-api` is enabled):

|SerialPortManagerImpl::OpenPort| [2] -> 
|BluetoothSerialDeviceEnumerator::BluetoothSerialDeviceEnumerator| [3] -> 
|BluetoothSerialDeviceEnumerator::AdapterHelper::AdapterHelper| [4] ->
|BluetoothSerialDeviceEnumerator::AdapterHelper::OnGotClassicAdapter| [5]

In [5], |BluetoothSerialDeviceEnumerator::AdapterHelper| add itself (`this` pointer) to the observer of adapter. The |BluetoothSerialDeviceEnumerator::AdapterHelper| class override two methods of BluetoothAdapter::Observer in [6], hence when the bluetooth device is added/removed, the corresponding method will be notified. 

However, |AdapterHelper| class only calls `AddObserver` function in [5], and doesn't call `RemoveObserver` function when it is destroyed, leading to the DeviceAdded/DeviceRemoved function of |AdapterHelper| is still called/notified after `AdapterHelper` instance is destroyed, causing the UAF in accessing freed |enumerator_runner_| and |enumerator_| object in [7].

To trigger the |GetDevices|, we could use |chrome.serial.getDevices| in an Chrome App, or |navigator.serial.getPorts| related api. However, freeing |AdapterHelper| (i.e., |SerialPortManagerImpl|, since it owns |AdapterHelper| indirectly) is not intuitive currently. Since the |SerialPortManagerImpl| is owned by |DeviceService| in [8], it might needs a shutdown to destroy |AdapterHelper|.

The exploit may strictly hard, the following chain might be work for UAF:

1. Enable enable-bluetooth-spp-in-serial-api feature.
2. Install an Chrome App. Calls `chrome.serial.getDevices(()=>{})` in the Chrome App. (This will trigger the AddObserver to the classic adapter)
3. Add/Remove bluetooth device while browser shutdown. (Not sure if the shutdown is necessar, since we only want to disconnect the mojo of SerialPortManagerImpl, an incognito context shutdown might be work.)
4. Trigger UAF while the Adapter notify the freed AdapterHelper.

Currently I haven't trigger that UAF since the condition of Add/Remove device during shutdown is a little bit tight. However, I've logged some free objects sequence messages with the above operation (adding logs to the ctor/dctor of the corresponding class) and the attached Chrome App (tested on Windows Chromium 105.0.5178.0):

[27496:25752:0715/232932.997:ERROR:bluetooth_adapter.cc(507)] on dtor BluetoothAdapter::~BluetoothAdapter: 00001219DE3A5F00
[27496:29512:0715/232942.505:ERROR:serial_port_manager_impl.cc(78)] on SerialDeviceEnumerator::Create
[27496:29512:0715/232942.506:ERROR:serial_port_manager_impl.cc(86)] will create bluetooth_enumerator_
[27496:25752:0715/232942.506:ERROR:bluetooth_serial_device_enumerator.cc(47)] on ctor BluetoothSerialDeviceEnumerator::AdapterHelper::AdapterHelper
[27496:25752:0715/232942.507:ERROR:bluetooth_serial_device_enumerator.cc(63)] on OnGotClassicAdapter, add observer to adapter: 00001215DE8D7D00
[27496:25752:0715/232942.512:INFO:CONSOLE(39)] "finish get devices.", source: chrome-extension://clejdddelpljocijkjpeafidbkkeecpe/background.js (39)
[27496:25752:0715/232946.072:ERROR:bluetooth_serial_device_enumerator.cc(103)] on dctor ~BluetoothSerialDeviceEnumerator
[27496:25752:0715/232946.073:ERROR:bluetooth_adapter.cc(507)] on dtor BluetoothAdapter::~BluetoothAdapter: 00001215DE8D7D00

We could notice that the |BluetoothSerialDeviceEnumerator| instance is freed prior to the |BluetoothAdapter|, hence during that tight window, the Add/Remove bluetooth device might has an chance to trigger the UAF.


[1]https://source.chromium.org/chromium/chromium/src/+/main:services/device/public/mojom/serial.mojom;l=148;drc=75425ebb5303c7bb416b2261e9b27114ec903d3f

[2]https://source.chromium.org/chromium/chromium/src/+/main:services/device/serial/serial_port_manager_impl.cc;l=97;drc=75425ebb5303c7bb416b2261e9b27114ec903d3f

void SerialPortManagerImpl::OpenPort(
    const base::UnguessableToken& token,
    bool use_alternate_path,
    device::mojom::SerialConnectionOptionsPtr options,
    mojo::PendingRemote<mojom::SerialPortClient> client,
    mojo::PendingRemote<mojom::SerialPortConnectionWatcher> watcher,
    OpenPortCallback callback) {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
  if (!enumerator_) {
    enumerator_ = SerialDeviceEnumerator::Create(ui_task_runner_);
    observed_enumerator_.AddObservation(enumerator_.get());
  }
  absl::optional<base::FilePath> path =
      enumerator_->GetPathFromToken(token, use_alternate_path);
  if (path) {
    io_task_runner_->PostTask(
        FROM_HERE,
        base::BindOnce(&SerialPortImpl::Open, *path, std::move(options),
                       std::move(client), std::move(watcher), ui_task_runner_,
                       base::BindOnce(&OnPortOpened, std::move(callback),
                                      base::SequencedTaskRunnerHandle::Get())));
    return;
  }

  if (base::CommandLine::ForCurrentProcess()->HasSwitch(
          switches::kEnableBluetoothSerialPortProfileInSerialApi)) {
    if (!bluetooth_enumerator_) {
      bluetooth_enumerator_ =
          std::make_unique<BluetoothSerialDeviceEnumerator>(ui_task_runner_); // [2] ----------- Construct BluetoothSerialDeviceEnumerator
      observed_enumerator_.AddObservation(bluetooth_enumerator_.get());
    }


[3]https://source.chromium.org/chromium/chromium/src/+/main:services/device/serial/bluetooth_serial_device_enumerator.cc;l=88;drc=75425ebb5303c7bb416b2261e9b27114ec903d3f

BluetoothSerialDeviceEnumerator::BluetoothSerialDeviceEnumerator(
    scoped_refptr<base::SingleThreadTaskRunner> adapter_runner) {
  DCHECK(base::CommandLine::ForCurrentProcess()->HasSwitch(
      switches::kEnableBluetoothSerialPortProfileInSerialApi));

  helper_ = base::SequenceBound<AdapterHelper>( // [3] ------------- Construct AdapterHelper
      std::move(adapter_runner), weak_ptr_factory_.GetWeakPtr(),
      base::SequencedTaskRunnerHandle::Get());
}

[4]https://source.chromium.org/chromium/chromium/src/+/main:services/device/serial/bluetooth_serial_device_enumerator.cc;l=42-50;drc=75425ebb5303c7bb416b2261e9b27114ec903d3f

BluetoothSerialDeviceEnumerator::AdapterHelper::AdapterHelper(
    base::WeakPtr<BluetoothSerialDeviceEnumerator> enumerator,
    scoped_refptr<base::SequencedTaskRunner> enumerator_runner)
    : enumerator_(std::move(enumerator)),
      enumerator_runner_(std::move(enumerator_runner)) {
  device::BluetoothAdapterFactory::Get()->GetClassicAdapter(base::BindOnce(
      &BluetoothSerialDeviceEnumerator::AdapterHelper::OnGotClassicAdapter, // [4] ------------- Call OnGotClassicAdapter once the classic adapter is prepared
      weak_ptr_factory_.GetWeakPtr()));
}


[5]https://source.chromium.org/chromium/chromium/src/+/main:services/device/serial/bluetooth_serial_device_enumerator.cc;l=52-66;drc=75425ebb5303c7bb416b2261e9b27114ec903d3f

void BluetoothSerialDeviceEnumerator::AdapterHelper::OnGotClassicAdapter(
    scoped_refptr<device::BluetoothAdapter> adapter) {
  SEQUENCE_CHECKER(sequence_checker_);
  DCHECK(adapter);

  BluetoothAdapter::DeviceList devices = adapter->GetDevices();
  for (auto* device : devices) {
    DeviceAdded(adapter.get(), device);
  }
  adapter->AddObserver(this); // [5] ------------- add |this| to the observer of adapter
  enumerator_runner_->PostTask(
      FROM_HERE,
      base::BindOnce(&BluetoothSerialDeviceEnumerator::SetClassicAdapter,
                     enumerator_, std::move(adapter)));
}

[6]https://source.chromium.org/chromium/chromium/src/+/main:services/device/serial/bluetooth_serial_device_enumerator.cc;l=29-32;drc=75425ebb5303c7bb416b2261e9b27114ec903d3f

  // BluetoothAdapter::Observer methods:
  void DeviceAdded(BluetoothAdapter* adapter, BluetoothDevice* device) override;
  void DeviceRemoved(BluetoothAdapter* adapter,
                     BluetoothDevice* device) override;

[7]https://source.chromium.org/chromium/chromium/src/+/main:services/device/serial/bluetooth_serial_device_enumerator.cc;l=68-86;drc=75425ebb5303c7bb416b2261e9b27114ec903d3f

void BluetoothSerialDeviceEnumerator::AdapterHelper::DeviceAdded(
    BluetoothAdapter*,
    BluetoothDevice* device) {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
  enumerator_runner_->PostTask(
      FROM_HERE,
      base::BindOnce(&BluetoothSerialDeviceEnumerator::DeviceAdded, enumerator_, // [7]
                     device->GetAddress(), device->GetNameForDisplay(),
                     device->GetUUIDs()));
}

void BluetoothSerialDeviceEnumerator::AdapterHelper::DeviceRemoved(
    BluetoothAdapter* adapter,
    BluetoothDevice* device) {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
  enumerator_runner_->PostTask(
      FROM_HERE, base::BindOnce(&BluetoothSerialDeviceEnumerator::DeviceRemoved, // [7]
                                enumerator_, device->GetAddress()));
}

[8]https://source.chromium.org/chromium/chromium/src/+/main:services/device/device_service.cc;l=122;drc=75425ebb5303c7bb416b2261e9b27114ec903d3f

### [Deleted User] (2022-07-15)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-07-17)

+reillyg, can you take a look? I can't see a strong reason why BluetoothAdaptor couldn't cause a UaF in the way described in the report, though it's a very unlikely scenario to trigger.

I'm assigning a none impact as this requires an off by default flag to be enabled. I'm also assigning a low severity as it requires a Chrome app to be installed and a very delicate setup.

[Monorail components: Blink>Serial Platform>Apps>API>Serial]

### re...@chromium.org (2022-07-18)

This UaF does seem reachable but it requires,

a) Enabling the disabled-by-default --enable-bluetooth-spp-in-serial-api flag.
b) Hitting a very narrow window which only occurs during browser shutdown.

This doesn't require a Chrome App, as this Mojo service is responsible for both the chrome.serial and web-exposed navigator.serial APIs. Shutdown issues can be triggered by Javascript if the script is able to close the last browser window.

The fix is to add two fields to the BluetoothSerialDeviceEnumerator::AdapterHelper class,

  scoped_refptr<BluetoothAdapter> adapter_;
  base::ScopedObservation<BluetoothAdapter, BluetoothAdapter::Observer> observation_{this};

Using a base::ScopedObservation will guarantee that RemoveObserver() is called on destruction. The scoped_refptr<BluetoothAdapter> is required to ensure that this object actually has a reference to the BluetoothAdapter when the call to RemoveObserver() happens.

### re...@chromium.org (2022-07-18)

Jack, can you take a look at implementing the fix above?

### do...@chromium.org (2022-07-19)

The alternative to adding scoped_refptr<BluetoothAdapter> adapter_ is to add a OnAdaptorWillBeDestroyed() method to the observer interface which gives the AdapterHelper a signal that the BluetoothAdapter is about to go away and to clear the scoped observation.

### he...@gmail.com (2022-08-31)

friendly ping -

### gi...@appspot.gserviceaccount.com (2022-09-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/182ec66ec13d18d532c0eb324e4af13969fc5574

commit 182ec66ec13d18d532c0eb324e4af13969fc5574
Author: Jack Hsieh <chengweih@chromium.org>
Date: Thu Sep 01 00:56:23 2022

[serial] Ensure RemoveObserver during BluetoothAdapter destruction

There is an UAF issue due to
BluetoothSerialDeviceEnumerator::AdapterHelper not remove itself from
observers of BluetoothAdapter and it ends up when
BluetoothSerialDeviceEnumerator::AdapterHelper is destroyed, the device
added/removed notified by BluetoothAdapter to its observers might lead
to UAF. This is fixed by using base::ScopedObservation so that
RemoveObserver can be called when
BluetoothSerialDeviceEnumerator::AdapterHelper destructs.

Bug: 1344878
Change-Id: Ib80ad45257caf0d9dedb0949e9de9cd39aee87ac
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3866838
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Jack Hsieh <chengweih@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1041839}

[modify] https://crrev.com/182ec66ec13d18d532c0eb324e4af13969fc5574/services/device/serial/bluetooth_serial_device_enumerator_unittests.cc
[modify] https://crrev.com/182ec66ec13d18d532c0eb324e4af13969fc5574/services/device/serial/bluetooth_serial_device_enumerator.cc


### ch...@chromium.org (2022-09-01)

Hi hedonistsmith@,

Sorry for the long wait on this. The fix has been submitted according to https://crbug.com/chromium/1344878#c8, the fix will be available in chrome 107.

### he...@gmail.com (2022-09-01)

[Comment Deleted]

### [Deleted User] (2022-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-07)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-07)

Congratulations! The VRP Panel has decided to award you $3,000 for this report of a moderately mitigated security bug. Thank you for your efforts in reporting this issue to us! 

### am...@google.com (2022-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-12-09)

This issue was migrated from crbug.com/chromium/1344878?no_tracker_redirect=1

[Multiple monorail components: Blink>Serial, Platform>Apps>API>Serial]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060298)*
