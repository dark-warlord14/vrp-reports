# BluetoothAdapterWin UAF Issue

| Field | Value |
|-------|-------|
| **Issue ID** | [450044213](https://issues.chromium.org/issues/450044213) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Windows |
| **Reporter** | va...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2025-10-08 |
| **Bounty** | $3,000.00 |

## Description

BluetoothAdapterWin is created through the BluetoothAdapterFactory::GetClassicAdapter interface. During creation, an object reference is retained within BluetoothAdapterFactory. After initialization is completed, init\_callback\_ is invoked. In this callback, the reference within BluetoothAdapterFactory is removed, and its own reference is passed to the caller for use. If the caller does not retain a reference to the adapter, the adapter's reference count will drop to zero and be destroyed after the execution of init\_callback\_, leading to a UAF issue in the subsequent logic of the BluetoothAdapterWin::AdapterStateChanged function.

Attached is the UAF information we captured online through GWP-ASAN.

```
void BluetoothAdapterWin::AdapterStateChanged(
    const BluetoothTaskManagerWin::AdapterState& state) {
  DCHECK(thread_checker_.CalledOnValidThread());
  name_ = state.name;
  bool was_present = IsPresent();
  bool is_present = !state.address.empty();
  address_ = CanonicalizeBluetoothAddress(state.address);
  if (was_present != is_present) {
    for (auto& observer : observers_)
      observer.AdapterPresentChanged(this, is_present);
  }
  if (powered_ != state.powered) {
    powered_ = state.powered;
    for (auto& observer : observers_)
      observer.AdapterPoweredChanged(this, powered_);
  }
  if (!initialized_) {
    initialized_ = true;
    std::move(init_callback_).Run(); // maybe destroy here.
  }

  // When the Bluetooth adapter is powered off or not present, all Bluetooth
  // devices should be removed.
  if (!powered_ || !is_present) {
    ClearAllDevices();
  }
}

```

## Attachments

- [gwp-asan-crash.txt](attachments/gwp-asan-crash.txt) (text/plain, 9.6 KB)
- [bt_classic_min_extension.zip](attachments/bt_classic_min_extension.zip) (application/zip, 2.5 KB)
- [Snipaste_2025-10-29_19-07-44.png](attachments/Snipaste_2025-10-29_19-07-44.png) (image/png, 107.1 KB)
- [Snipaste_2025-10-29_19-08-10.png](attachments/Snipaste_2025-10-29_19-08-10.png) (image/png, 1.7 MB)
- [20251029-190452.mp4](attachments/20251029-190452.mp4) (video/mp4, 11.0 MB)

## Timeline

### ch...@google.com (2025-10-11)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ah...@google.com (2025-10-13)

[Security Shepherd]

Provisionally setting foundIn to the current extended stable, platform to windows.

@ma...@chromium.org, could you please check whether this can be reliably reached?

thanks,

### al...@google.com (2025-10-13)

Actually the attempt fix (crrev.com/c/7019630) has been merged. 
Somehow it is not updated here probably due to the change is using incorrect syntax to link the bug.

### ch...@google.com (2025-10-14)

Setting milestone because of s2 severity.

### ch...@google.com (2025-10-28)

mattreynolds: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ma...@chromium.org (2025-10-28)

Hi Alvin, can you check if this was reachable without the fix?

### al...@chromium.org (2025-10-28)

Hi @va...@gmail.com,

Do you have a demo site or script that we can use to reproduce this? Or have you verified the fix and can confirm whether [crrev.com/c/7019630](https://crrev.com/c/7019630) fix it?

Thanks!  

Alvin

### va...@gmail.com (2025-10-29)

I have created a sample extension to reproduce this issue. The reproduction steps are as follows:

1. Enable Developer mode in Chrome's Extensions page.
2. Load this sample extension.
3. Click the "Listen with invalid UUID" button in the extension's popup window.

It should be noted that this UAF (Use-After-Free) issue does not always cause a crash, and a debugger can be used to verify it.

Test Chrome version：141.0.7390.123 (Official Build) (64-bit) (cohort: Stable Installs & Version Pins) .

And yes, I have confirmed that the fix（[crrev.com/c/7019630](https://crrev.com/c/7019630)）can resolves the issue.

### al...@chromium.org (2025-11-01)

Thanks for sharing the repro case, I can also confirm that the repro case does crash on ASAN build and the fix ([crrev.com/c/7019630](https://crrev.com/c/7019630)) solve it.

### ch...@google.com (2025-11-01)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-11-01)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2025-11-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
a moderately mitigated (due to pre-requisites) memory corruption in a non-sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-02-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> a moderately mitigated (due to pre-requisites) memory corruption in a non-sandboxed process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/450044213)*
