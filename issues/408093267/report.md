# Chrome : WebGL DrawArrays Kernel Use-After-Free

| Field | Value |
|-------|-------|
| **Issue ID** | [408093267](https://issues.chromium.org/issues/408093267) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL |
| **Platforms** | Linux |
| **Chrome Version** | 134.0.0.0 |
| **Reporter** | xi...@gmail.com |
| **Assignee** | kb...@chromium.org |
| **Created** | 2025-04-03 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. open chrome ( ./chrome --no-sandbox uaf.html uaf.html uaf.html )
2. load html file
3. log read ( sudo dmesg )

# Problem Description

Kernel Version : 6.11.0-19-generic GPU & CPU : ryzen5-7530U

When a WebGL kernel timeout occurs, the AMD GPU driver attempts to recover. However, during the recovery process, the reference counter underflows, leading to a use-after-free issue.

You can intentionally cause a webgl timeout, resulting in a Use-After-Free in the Kernel.

Chromium should be limited in size to drawarrays for amd gpu targets.
Since the use-after-free (UAF) occurs in the kernel, this vulnerability can be exploited as a sandbox escape.

# Additional Comments

Please Check Reproduce Video

# Summary

Chrome : WebGL DrawArrays Kernel Use-After-Free

# Custom Questions

#### Type of crash:

etc

#### Reporter credit:

31313131

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [IMG_2208.MOV](attachments/IMG_2208.MOV) (video/quicktime, 78.1 MB)
- [uaf (1).html](attachments/uaf (1).html) (text/html, 5.4 KB)
- [crash.out](attachments/crash.out) (application/octet-stream, 149.0 KB)

## Timeline

### xi...@gmail.com (2025-04-03)

Crash log

### nh...@chromium.org (2025-04-03)

kbr: Can you look at this and see if a shader workaround is appropriate here? [crbug.com/407645758](https://crbug.com/407645758) is a very similar report, but neither of them demonstrate code execution in chrome or other security impact.

### li...@chromium.org (2025-04-03)

This does look to me like from Chrome's perspective this is a DoS, since the PoC triggers a timeout.

I'm not entirely convinced from the crash log that there's a UaF in the AMD driver, reporter could you clarify where you see the underflow happening and where in the crash log there's evidence of a UaF?

kbr@ are there relevant AMD folks we could add to this? There's a chance this might be a functionality bug but it will heavily depend on whether the driver crash presents the opportunity for an attacker to place attacker controlled data, and I think someone from their team will be better equipped to assess that.

### kb...@chromium.org (2025-04-03)

If I'm understanding correctly, the following excerpt from `crash.out` indicates a UAF in AMD's driver:

```
[  609.562798] refcount_t: underflow; use-after-free.
[  609.562804] WARNING: CPU: 0 PID: 95 at lib/refcount.c:28 refcount_warn_saturate+0xfb/0x150
[  609.562807] Modules linked in: xt_conntrack nft_chain_nat xt_MASQUERADE nf_nat nf_conntrack_netlink nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 xfrm_user xfrm_algo xt_addrtype nft_compat nf_tables libcrc32c br_netfilter bridge stp llc rfcomm snd_seq_dummy snd_hrtimer overlay qrtr cmac algif_hash algif_skcipher af_alg bnep binfmt_misc amd_atl intel_rapl_msr nls_iso8859_1 intel_rapl_common snd_sof_amd_acp63 snd_sof_amd_vangogh snd_sof_amd_rembrandt snd_sof_amd_renoir snd_sof_amd_acp snd_sof_pci snd_sof_xtensa_dsp amdgpu edac_mce_amd snd_sof snd_sof_utils snd_pci_ps snd_hda_codec_realtek snd_amd_sdw_acpi kvm_amd snd_hda_codec_generic soundwire_amd soundwire_generic_allocation snd_hda_scodec_component soundwire_bus ee1004 snd_hda_codec_hdmi kvm snd_soc_core snd_hda_intel crct10dif_pclmul snd_intel_dspcfg snd_compress rtw89_8852be polyval_clmulni snd_intel_sdw_acpi ac97_bus rtw89_8852b polyval_generic snd_pcm_dmaengine snd_hda_codec ghash_clmulni_intel rtw89_8852b_common snd_rpl_pci_acp6x snd_hda_core sha256_ssse3 rtw89_pci
[  609.562881]  uvcvideo snd_acp_pci amdxcp snd_hwdep sha1_ssse3 drm_exec videobuf2_vmalloc snd_acp_legacy_common snd_seq_midi aesni_intel rtw89_core gpu_sched uvc snd_pci_acp6x snd_seq_midi_event btusb crypto_simd drm_buddy videobuf2_memops cryptd btrtl think_lmi snd_rawmidi videobuf2_v4l2 drm_suballoc_helper snd_pcm btintel drm_ttm_helper rapl firmware_attributes_class mac80211 videodev snd_pci_acp5x wmi_bmof ttm btbcm snd_seq snd_rn_pci_acp3x drm_display_helper btmtk videobuf2_common snd_seq_device snd_acp_config snd_timer cec bluetooth snd_soc_acpi mc rc_core cfg80211 snd ccp ideapad_laptop snd_pci_acp3x i2c_piix4 i2c_algo_bit soundcore sparse_keymap libarc4 k10temp i2c_smbus platform_profile input_leds amd_pmc joydev serio_raw mac_hid sch_fq_codel msr parport_pc ppdev lp parport efi_pstore nfnetlink dmi_sysfs ip_tables x_tables autofs4 hid_multitouch hid_generic nvme ucsi_acpi sdhci_pci i2c_hid_acpi xhci_pci nvme_core typec_ucsi video cqhci crc32_pclmul i2c_hid xhci_pci_renesas nvme_auth sdhci typec wmi hid
[  609.562975] CPU: 0 UID: 0 PID: 95 Comm: kworker/u48:2 Tainted: G        W          6.11.0-19-generic #19~24.04.1-Ubuntu
[  609.562978] Tainted: [W]=WARN
[  609.562980] Hardware name: LENOVO 82XM/LNVNB161216, BIOS KYCN31WW 03/18/2024
[  609.562982] Workqueue: amdgpu-reset-dev drm_sched_job_timedout [gpu_sched]
[  609.562986] RIP: 0010:refcount_warn_saturate+0xfb/0x150
[  609.562989] Code: eb 9a 0f b6 1d 13 cf 16 02 80 fb 01 0f 87 b0 7e 9a 00 83 e3 01 75 85 48 c7 c7 a8 a2 ce 90 c6 05 f7 ce 16 02 01 e8 15 d4 86 ff <0f> 0b e9 6b ff ff ff 0f b6 1d e5 ce 16 02 80 fb 01 0f 87 6d 7e 9a
[  609.562991] RSP: 0018:ffff9d9580473c68 EFLAGS: 00010246
[  609.562994] RAX: 0000000000000000 RBX: 0000000000000000 RCX: 0000000000000000
[  609.562996] RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
[  609.562997] RBP: ffff9d9580473c70 R08: 0000000000000000 R09: 0000000000000000
[  609.562999] R10: 0000000000000000 R11: 0000000000000000 R12: ffff904c9fc80000
[  609.563000] R13: 0000000000000000 R14: ffff904e2bc79800 R15: ffff9d9580473da0
[  609.563002] FS:  0000000000000000(0000) GS:ffff904f1fc00000(0000) knlGS:0000000000000000
[  609.563004] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[  609.563006] CR2: 000070c5bd5aa000 CR3: 000000017d43e000 CR4: 0000000000f50ef0
[  609.563008] PKRU: 55555554
[  609.563010] Call Trace:
[  609.563011]  <TASK>
[  609.563012]  ? show_regs+0x6c/0x80
[  609.563016]  ? __warn+0x88/0x140
[  609.563019]  ? refcount_warn_saturate+0xfb/0x150
[  609.563022]  ? report_bug+0x182/0x1b0
[  609.563026]  ? handle_bug+0x6e/0xb0
[  609.563030]  ? exc_invalid_op+0x18/0x80
[  609.563033]  ? asm_exc_invalid_op+0x1b/0x20
[  609.563039]  ? refcount_warn_saturate+0xfb/0x150
[  609.563042]  ? refcount_warn_saturate+0xfb/0x150
[  609.563044]  amdgpu_vm_put_task_info+0x4e/0x60 [amdgpu]
[  609.563239]  amdgpu_coredump+0xc8/0x150 [amdgpu]
[  609.563482]  amdgpu_do_asic_reset+0x5b6/0x660 [amdgpu]
[  609.563812]  amdgpu_device_gpu_recover+0x5a2/0xae0 [amdgpu]
[  609.564001]  amdgpu_job_timedout+0x150/0x220 [amdgpu]
[  609.564259]  drm_sched_job_timedout+0x70/0x110 [gpu_sched]
[  609.564265]  process_one_work+0x17b/0x3d0
[  609.564270]  worker_thread+0x2de/0x410
[  609.564273]  ? __pfx_worker_thread+0x10/0x10
[  609.564276]  kthread+0xe4/0x110
[  609.564279]  ? __pfx_kthread+0x10/0x10
[  609.564282]  ret_from_fork+0x47/0x70
[  609.564284]  ? __pfx_kthread+0x10/0x10
[  609.564287]  ret_from_fork_asm+0x1a/0x30
[  609.564294]  </TASK>

```

For the record, the test case locks up my MacBook Pro requiring a hard reset. From that standpoint it's a Denial of Service and not a security bug, but if this crash on AMD hardware is attacker-controllable then that would be a security issue.

### li...@chromium.org (2025-04-03)

Ah thanks for that, I didn't see that in the crash log when I grepped.

It's still not clear whether this is attacker-controllable in AMD hardware.
Reporter: did you report this bug to AMD as well? If not, can you please file a bug with them?

### kb...@chromium.org (2025-04-03)

Note that Paul Blinzer from AMD is CC'd and he has confirmed he's filed an internal ticket at AMD about this.

### kb...@chromium.org (2025-04-03)

Was this reported separately as [Issue 407645758](https://issues.chromium.org/issues/407645758)?

### xi...@gmail.com (2025-04-04)

It's the same thing.

I sent it again after poc minimization.

### pe...@google.com (2025-04-04)

Thank you for providing more feedback. Adding the requester to the CC list.

### kb...@chromium.org (2025-04-07)

Submitter, the suggestion to "limit the size of DrawArrays calls on AMD GPUs" - can you clarify what you mean, and what in your opinion would be a suitable workaround for this bug?

### xi...@gmail.com (2025-04-07)

The root cause of this issue is that a large resource allocation in the GPU kernel driver leads to a timeout, which subsequently causes a use-after-free vulnerability.

Therefore, it is advisable to avoid operations that put excessive strain on the GPU kernel driver. A representative example is using a large count value in functions such as drawArraysInstanced (`drawArraysInstanced(mode, first, count, instanceCount)`). When using AMDGPU, validating the count parameter in functions like drawArraysInstanced or drawArrays to prevent GPU kernel driver timeouts would be a practical workaround.

but the most proper and fundamental solution would be for AMD to patch this bug directly.

### pe...@google.com (2025-04-07)

Thank you for providing more feedback. Adding the requester to the CC list.

### ma...@google.com (2025-04-11)

Based on this being a kernel UAF that can be reached from the web, I'm going to triage this Critical severity for now. Though IIUC, the question whether this is attacker controllable is still unresolved?

### ch...@google.com (2025-04-11)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-04-11)

Setting Priority to P0 to match Severity s0. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### kb...@chromium.org (2025-04-22)

Submitter - Chrome already validates all incoming parameters to functions like `drawArraysInstanced`. There is no practical limit which could be introduced on the number of primitives or number of instances in that function call. If the root cause is a GPU timeout which AMD's driver is handling incorrectly, then it should be easy to modify the shader to take a long time, and draw relatively few primitives/instances, to produce a similar GPU hang.

If you could help verify this assertion I would appreciate it, since I can't reproduce the problem on the hardware I have available.

We also need to know whether you think this crash is attacker-controllable.

### xi...@gmail.com (2025-04-22)

1. -> I agree with this part as well.
   Even beyond the drawArrays function, if a shader or other function is induced to allocate excessive resources, a Kernel GPU Hang can, in some ways, occur relatively easily.
2. -> My own approach, which involves triggering a kernel panic from within HTML, has many limitations. Therefore, if an attacker possesses an exploit for this kernel panic bug, and if a GPU process exploit also exists, it's possible that they could first exploit the GPU process and then leverage its privileges to launch a kernel exploit, potentially enabling a sandbox escape.

### li...@chromium.org (2025-04-28)

I'm downgrading this to an S1 for now since it seems like a secondary exploit, either a kernel bug or a GPU process bug, is likely to be necessary even if this crash is attacker-controllable.

Are there by chance any updates from AMD about this, since they have an internal ticket for this as well?

### ap...@gmail.com (2025-04-29)

After some investigation, we believe that the upstreamed fix here: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=8d1a13816e59254bd3b18f5ae0895230922bd120 is fixing this issue already. 
As soon as the distributions are picking up this change, the problem should be addressed. 

### li...@chromium.org (2025-04-29)

It looks like 6.12.7 is the [earliest kernel version](https://elixir.bootlin.com/linux/v6.12.7/source/drivers/gpu/drm/amd/amdgpu/amdgpu_dev_coredump.c#L348) that has the patch from [#comment20](https://issues.chromium.org/issues/408093267#comment20).

Reporter: is it possible for you to update the kernel version on your distro and confirm if your PoC still works? Or patch in the above commit?

I'm also going to keep this as a vulnerability with high severity as looking through the fix it does appear that this was a UAF that occurred before refcount protections could have kicked in, so it is likely this could be attacker controlled.

### xi...@gmail.com (2025-05-01)

I checked the patch, and it seems to have been applied correctly. I also tested this PoC on kernel version 13, and the use-after-free issue does not reproduce.

### ch...@google.com (2025-05-06)

kbr: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### li...@chromium.org (2025-05-06)

Okay so this does look fixed in the patch mentioned in [#comment20](https://issues.chromium.org/issues/408093267#comment20).

apblinzer@: it looks like the coredump code has gone through a bunch of refactoring semi-recently, so it doesn't seem possible to directly backport the patch to older kernel versions, but is it still possible to patch a similar fix?

For example, 6.6 is still an LTS kernel and receiving security updates, and the coredump code in that kernel version still [reads the VM pointer](https://elixir.bootlin.com/linux/v6.6.87/source/drivers/gpu/drm/amd/amdgpu/amdgpu_device.c#L4995), so it would be good to backport this patch somehow into kernel versions that are still scheduled for security fixes.

### ap...@gmail.com (2025-05-06)

I will need to check with our Linux developers, but this may require coordination with the various distro's. Any particular prioritization from your side? 

### ch...@google.com (2025-05-07)

kbr: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-07)

kbr: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-08)

kbr: Uh oh! This issue still open and hasn't been updated in the last 16 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pg...@google.com (2025-05-08)

(sorry about the spam - [issue 413695648](https://issues.chromium.org/issues/413695648) has been filed to fix the blintz rule's spammyness)

### li...@chromium.org (2025-05-09)

Ah I must apologize as I got a bit ahead of myself. Actually, since this patch has been upstreamed we (Chrome security) can consider this bug fixed from our side, as recommending porting fixes outside of chrome is out of scope for us.

So to answer your question in [#comment25](https://issues.chromium.org/issues/408093267#comment25) we don't have any prioritization at all, and I'm actually going to mark this bug as fixed from our perspective.

### xi...@gmail.com (2025-05-09)

Thank you for your efforts regarding this bug.

### ch...@google.com (2025-05-09)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-05-10)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M136. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M137. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [136, 137].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2025-05-12)

This is a GPU driver issue and was resolved upstream by AMD; Chromium mergers are n/a for this issue.

### ap...@gmail.com (2025-05-13)

An update from our Linux developers on this issue for the older kernel backport: 
As you are aware there was a lot of code refactoring happening in the code region between the current kernels where this fix applies and some older kernel versions, so a direct backport is not possible. The issue was caused by the structure(s) that were accessed when printing the name of the process the GPU hang occurred on not being properly reference counted. This is what the Kernel update fixes, essentially. 
But on older kernels that was not even reference counted in the first place. Redesigning the fix to older kernel is a substantial effort and it is not clear if this issue has a relevant security impact, as at that time the affected context is destined for further cleanup anyway. 

In the scenario the log may see some garbage text and at most a potential DoS of that graphics context, but there shouldn't be an opportunity to use that freed memory for interesting things, from the looks of the code. 

What kernel versions would need to be considered for a backport, as we would have to work with the maintainers and adapt this for several different kernels? 

### ap...@gmail.com (2025-05-14)

To give a little more info here, the specific "use after free" issue was first introduced into the 6.10 kernel stream, previous kernel releases did not have the "use after free" scenario, but in some cases would have produced some bad log output accessing resident memory state. 
The problem was introduced by a reference count value to address the garbage output, which was part of dynamically allocated memory structures that in some specific scenarios may have been freed before the printk() functions was executed. 

The "use after free" issue is fixed for 6.13 kernels and it was backported to the  6.12.7 kernel revisions. 6.10 and 6.11 kernel streams are EOLed and these kernel streams are not accepting any backports. Insofar the issue should be fully addressed provided the distributions are including the proper, still maintained kernel streams. 

From the AMD side the issue is now fully addressed to the extent it can be from our side and so this ticket should be ready to be closed. 
Let us know if there is any further question or concern. 

### xi...@gmail.com (2025-05-16)

Okay Thank you!

### sp...@google.com (2025-05-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Thank you report for this report of an issue known and resolved by AMD, resolved by an upstream change in December 2024, resulting in backporting of this fix to some active kernel versions. 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-05-16)

Thanks again for this report. Since this was resolved upstream [1] in the kernel back in December, this would generally count of a previously known issue. Because your report did result in some backmerge decisions related to the potential for exploitability, we did want to thank you via a small reward. We appreciate your efforts and reporting this issue to us so that could occur.

[1] <https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=8d1a13816e59254bd3b18f5ae0895230922bd120>

### xi...@gmail.com (2025-05-21)

Thank you !

### ch...@google.com (2025-08-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Thank you report for this report of an issue known and resolved by AMD, resolved by an upstream change in December 2024, resulting in backporting of this fix to some active kernel versions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/408093267)*
