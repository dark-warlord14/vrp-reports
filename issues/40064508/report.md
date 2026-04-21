# Security: A use after free vulnerability exists in ChromeOS Kernel

| Field | Value |
|-------|-------|
| **Issue ID** | [40064508](https://issues.chromium.org/issues/40064508) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | ay...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-05-11 |
| **Bounty** | $15,000.00 |

## Description

Google Chrome: Version 113.0.5672.114 (Official Build)  (64-bit)
Platform: 15393.48.0 (Official Build) stable-channel reven
Channel: stable-channel
Firmware Version: 
ARC Enabled: false
ARC: 
Enterprise Enrolled: false
Developer Mode: true
Chrome OS Platform: <ChromeOS Flex>

The issue exists in the esdfs subsystem of the Linux kernel.

Steps To Reproduce:
(1) First compile the poc.c file. gcc poc.c -o poc --static
(2) Copy the poc file to the /usr/local directory of ChromeOS
(3) execute ./poc in root shell.

Expected Result:

Wait a few minutes and ChromeOS will crash, causing a reboot

How frequently does this problem reproduce? (Always, sometimes, hard to
reproduce?)

There is always a crash, after waiting for a few minutes.

What is the impact to the user, and is there a workaround? If so, what is
it?

A user who can mount a disk can escalate privileges to the kernel through this vulnerability

Please provide any additional information below. Attach a screen shot or
log if possible.

KASAN log is below

[   88.440410][ T2031] ==================================================================
[   88.440978][ T2031] BUG: KASAN: use-after-free in __hlist_bl_del+0xc4/0xd2
[   88.441354][ T2031] Write of size 8 at addr ffff88801f82c1c0 by task poc/2031
[   88.441406][T22275] ESDFS-fs (esdfs): mounted on top of ./file0 type ext4
[   88.441724][ T2031] 
[   88.442215][ T2031] CPU: 1 PID: 2031 Comm: poc Not tainted 5.15.98-17014-gafcfaad79298 #10 ca578080b09dff66884d898a62200c13e25b602a
[   88.442819][ T2031] Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS 1.15.0-1 04/01/2014
[   88.443280][ T2031] Call Trace:
[   88.443450][ T2031]  <TASK>
[   88.443603][ T2031]  dump_stack_lvl+0xcd/0x134
[   88.443846][ T2031]  print_address_description.constprop.0+0x1f/0x27d
[   88.444199][ T2031]  ? __hlist_bl_del+0xc4/0xd2
[   88.444447][ T2031]  kasan_report+0x174/0x1b5
[   88.444692][ T2031]  ? __hlist_bl_del+0xc4/0xd2
[   88.444942][ T2031]  __hlist_bl_del+0xc4/0xd2
[   88.445197][ T2031]  ___d_drop+0xb0/0xba
[   88.445419][ T2031]  __d_drop+0x40/0x95
[   88.445630][ T2031]  d_drop+0x22/0x2d
[   88.445832][ T2031]  do_one_tree+0x2b/0x34
[   88.446057][ T2031]  shrink_dcache_for_umount+0x7e/0xfb
[   88.446342][ T2031]  generic_shutdown_super+0x68/0x388
[   88.446473][T22284] ESDFS-fs (esdfs): mounted on top of ./file0 type ext4
[   88.446965][ T2031]  kill_anon_super+0x3b/0x43
[   88.447209][ T2031]  deactivate_locked_super+0x90/0xd1
[   88.447487][ T2031]  deactivate_super+0xaa/0xb5
[   88.447737][ T2031]  cleanup_mnt+0x103/0x211
[   88.447856][T22283] ESDFS-fs (esdfs): mounted on top of ./file0 type ext4
[   88.447971][ T2031]  task_work_run+0x12b/0x160
[   88.448387][T22282] ESDFS-fs (esdfs): mounted on top of ./file0 type ext4
[   88.448557][ T2031]  exit_to_user_mode_prepare+0xc4/0x1cb
[   88.449199][ T2031]  syscall_exit_to_user_mode+0x18/0x52
[   88.449218][ T2031]  do_syscall_64+0xa6/0xac
[   88.449563][T22280] ESDFS-fs (esdfs): mounted on top of ./file0 type ext4
[   88.449841][ T2031]  entry_SYSCALL_64_after_hwframe+0x61/0xcb
[   88.450519][ T2031] RIP: 0033:0x44d50b
[   88.450814][ T2031] Code: 07 00 48 83 c4 08 5b 5d c3 66 0f 1f 44 00 00 c3 66 2e 0f 1f 84 00 00 00 00 00 0f 1f 44 00 00 f3 0f 1e fa b8 a6 00 00 00 0f 05 <48> 3d 00 f0 ff ff 77 05 c3 0f 1f 40 08
[   88.451989][T22286] ESDFS-fs (esdfs): mounted on top of ./file0 type ext4
[   88.452211][ T2031] RSP: 002b:00007ffcbb7c4b18 EFLAGS: 00000206 ORIG_RAX: 00000000000000a6
[   88.453181][ T2031] RAX: 0000000000000000 RBX: 00007ffcbb7c5e68 RCX: 000000000044d50b
[   88.453761][ T2031] RDX: 0000000000000000 RSI: 000000000000000a RDI: 00007ffcbb7c4bf0
[   88.454342][ T2031] RBP: 00007ffcbb7c5c00 R08: 0000000000000000 R09: 00007ffcbb7c49b0
[   88.454922][ T2031] R10: 00000000023fe88b R11: 0000000000000206 R12: 0000000000000001
[   88.455503][ T2031] R13: 00007ffcbb7c5e58 R14: 00000000004c6770 R15: 0000000000000001
[   88.456096][ T2031]  </TASK>
[   88.456323][ T2031] 
[   88.456502][ T2031] Allocated by task 22251:
[   88.456857][ T2031]  kasan_save_stack+0x1b/0x3c
[   88.457268][ T2031]  kasan_set_track+0x1c/0x21
[   88.457671][ T2031]  __kasan_slab_alloc+0x6b/0x75
[   88.458051][ T2031]  slab_post_alloc_hook+0x4c/0x1ce
[   88.458444][ T2031]  kmem_cache_alloc+0x148/0x22c
[   88.458853][ T2031]  __d_alloc+0x28/0x738
[   88.459217][ T2031]  d_make_root+0x40/0x73
[   88.459586][ T2031]  __esdfs_fill_super+0x12c9/0x228c
[   88.459963][ T2031]  mount_nodev+0x64/0xff
[   88.460190][ T2031]  esdfs_mount+0x8e/0xb4
[   88.460418][ T2031]  legacy_get_tree+0x109/0x1a3
[   88.460675][ T2031]  vfs_get_tree+0x8d/0x2c1
[   88.460910][ T2031]  path_mount+0x1100/0x12f2
[   88.461151][ T2031]  do_mount+0xcc/0x123
[   88.461370][ T2031]  __do_sys_mount+0x235/0x270
[   88.461621][ T2031]  do_syscall_64+0x8a/0xac
[   88.461855][ T2031]  entry_SYSCALL_64_after_hwframe+0x61/0xcb
[   88.462167][ T2031] 
[   88.462289][ T2031] Freed by task 21:
[   88.462486][ T2031]  kasan_save_stack+0x1b/0x3c
[   88.462734][ T2031]  kasan_set_track+0x1c/0x21
[   88.462978][ T2031]  kasan_set_free_info+0x20/0x2f
[   88.463237][ T2031]  ____kasan_slab_free+0xfd/0x119
[   88.463501][ T2031]  slab_free_freelist_hook+0x111/0x16c
[   88.463808][ T2031]  kmem_cache_free+0x6f/0x211
[   88.464083][ T2031]  rcu_core+0x807/0xd43
[   88.464314][ T2031]  __do_softirq+0x2df/0x661
[   88.464551][ T2031] 
[   88.464677][ T2031] Last potentially related work creation:
[   88.464973][ T2031]  kasan_save_stack+0x1b/0x3c
[   88.465224][ T2031]  kasan_record_aux_stack+0x10a/0x110
[   88.465517][ T2031]  call_rcu+0x130/0x57d
[   88.465741][ T2031]  dentry_free+0x10e/0x117
[   88.465973][ T2031]  __dentry_kill+0x3e3/0x40e
[   88.466221][ T2031]  dput+0x2cd/0x329
[   88.466421][ T2031]  shrink_dcache_for_umount+0x7e/0xfb
[   88.466705][ T2031]  generic_shutdown_super+0x68/0x388
[   88.466981][ T2031]  kill_anon_super+0x3b/0x43
[   88.467220][ T2031]  deactivate_locked_super+0x90/0xd1
[   88.467496][ T2031]  deactivate_super+0xaa/0xb5
[   88.467740][ T2031]  cleanup_mnt+0x103/0x211
[   88.467976][ T2031]  task_work_run+0x12b/0x160
[   88.468218][ T2031]  exit_to_user_mode_prepare+0xc4/0x1cb
[   88.468509][ T2031]  syscall_exit_to_user_mode+0x18/0x52
[   88.468804][ T2031]  do_syscall_64+0xa6/0xac
[   88.469039][ T2031]  entry_SYSCALL_64_after_hwframe+0x61/0xcb
[   88.469350][ T2031] 
[   88.469474][ T2031] Second to last potentially related work creation:
[   88.469807][ T2031]  kasan_save_stack+0x1b/0x3c
[   88.470052][ T2031]  kasan_record_aux_stack+0x10a/0x110
[   88.470330][ T2031]  call_rcu+0x130/0x57d
[   88.470549][ T2031]  dentry_free+0x10e/0x117
[   88.470779][ T2031]  __dentry_kill+0x3e3/0x40e
[   88.471019][ T2031]  shrink_dentry_list+0x27d/0x295
[   88.471293][ T2031]  shrink_dcache_parent+0x215/0x25f
[   88.471571][ T2031]  vfs_rmdir+0x18e/0x25f
[   88.471793][ T2031]  do_rmdir+0x272/0x35e
[   88.472013][ T2031]  __x64_sys_rmdir+0x3e/0x42
[   88.472256][ T2031]  do_syscall_64+0x8a/0xac
[   88.472489][ T2031]  entry_SYSCALL_64_after_hwframe+0x61/0xcb
[   88.472802][ T2031] 
[   88.472926][ T2031] The buggy address belongs to the object at ffff88801f82c178
[   88.472926][ T2031]  which belongs to the cache dentry of size 312
[   88.473608][ T2031] The buggy address is located 72 bytes inside of
[   88.473608][ T2031]  312-byte region [ffff88801f82c178, ffff88801f82c2b0)
[   88.474276][ T2031] The buggy address belongs to the page:
[   88.474562][ T2031] page:ffffea00007e0b00 refcount:1 mapcount:0 mapping:0000000000000000 index:0x0 pfn:0x1f82c
[   88.475073][ T2031] head:ffffea00007e0b00 order:1 compound_mapcount:0
[   88.475410][ T2031] flags: 0x4000000000010200(slab|head|zone=1)
[   88.475726][ T2031] raw: 4000000000010200 ffffea00007bd280 0000000500000005 ffff88800a9b1780
[   88.476162][ T2031] raw: 0000000000000000 0000000000150015 00000001ffffffff 0000000000000000
[   88.476592][ T2031] page dumped because: kasan: bad access detected
[   88.476921][ T2031] page_owner tracks the page as allocated
[   88.477210][ T2031] page last allocated via order 1, migratetype Reclaimable, gfp_mask 0xd20d0(__GFP_IO|__GFP_FS|__GFP_NOWARN|__GFP_NORETRY|__GFP_COMP|__GFP_NOMEMALLOC|__GFP_RECLAIMABLE), pid5
[   88.478259][ T2031]  prep_new_page+0x17/0x62
[   88.478492][ T2031]  get_page_from_freelist+0xa95/0xbe8
[   88.478770][ T2031]  __alloc_pages+0x15a/0x382
[   88.479011][ T2031]  new_slab+0x93/0x3ef
[   88.479228][ T2031]  ___slab_alloc.constprop.0+0x805/0x958
[   88.479529][ T2031]  __slab_alloc.constprop.0+0x54/0x7d
[   88.479809][ T2031]  kmem_cache_alloc+0xb6/0x22c
[   88.480098][ T2031]  __d_alloc+0x28/0x738
[   88.480429][ T2031]  d_alloc+0x40/0xdb
[   88.480639][ T2031]  __lookup_hash+0xb6/0x143
[   88.480899][ T2031]  filename_create+0x1fd/0x39c
[   88.481258][ T2031]  do_mkdirat+0xa7/0x288
[   88.481580][ T2031]  __x64_sys_mkdir+0x65/0x6a
[   88.481927][ T2031]  do_syscall_64+0x8a/0xac
[   88.482262][ T2031]  entry_SYSCALL_64_after_hwframe+0x61/0xcb
[   88.482704][ T2031] page last free stack trace:
[   88.483046][ T2031]  free_unref_page_prepare+0x28c/0x47e
[   88.483455][ T2031]  free_unref_page+0x28/0x152
[   88.483807][ T2031]  __unfreeze_partials+0x109/0x11d
[   88.484193][ T2031]  qlist_free_all+0xae/0xe1
[   88.484534][ T2031]  kasan_quarantine_reduce+0x10d/0x143
[   88.484948][ T2031]  __kasan_slab_alloc+0x1c/0x75
[   88.485319][ T2031]  slab_post_alloc_hook+0x4c/0x1ce
[   88.485706][ T2031]  kmem_cache_alloc+0x148/0x22c
[   88.486074][ T2031]  getname_flags+0x6b/0x40b
[   88.486417][ T2031]  do_sys_openat2+0xa2/0x3ed
[   88.486769][ T2031]  do_sys_open+0x8d/0xc1
[   88.487107][ T2031]  do_syscall_64+0x8a/0xac
[   88.487491][ T2031]  entry_SYSCALL_64_after_hwframe+0x61/0xcb
[   88.487998][ T2031] 
[   88.488202][ T2031] Memory state around the buggy address:
[   88.488682][ T2031]  ffff88801f82c080: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
[   88.489359][ T2031]  ffff88801f82c100: 00 00 00 00 00 00 00 fc fc fc fc fc fc fc fc fa
[   88.489806][ T2031] >ffff88801f82c180: fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb
[   88.490218][ T2031]                                            ^
[   88.490535][ T2031]  ffff88801f82c200: fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb
[   88.490958][ T2031]  ffff88801f82c280: fb fb fb fb fb fb fc fc fc fc fc fc fc fc 00 00
[   88.491368][ T2031] ==================================================================
[   88.491775][ T2031] Disabling lock debugging due to kernel taint
[   88.492191][ T2031] Kernel panic - not syncing: KASAN: panic_on_warn set ...
[   88.492564][ T2031] CPU: 1 PID: 2031 Comm: poc Tainted: G    B             5.15.98-17014-gafcfaad79298 #10 ca578080b09dff66884d898a62200c13e25b602a
[   88.493248][ T2031] Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS 1.15.0-1 04/01/2014
[   88.493763][ T2031] Call Trace:
[   88.493934][ T2031]  <TASK>
[   88.494093][ T2031]  dump_stack_lvl+0xcd/0x134
[   88.494337][ T2031]  panic+0x2c4/0x6ca
[   88.494551][ T2031]  ? __warn_printk+0xf3/0xf3
[   88.494794][ T2031]  ? asm_sysvec_apic_timer_interrupt+0x16/0x20
[   88.495116][ T2031]  ? __hlist_bl_del+0xc4/0xd2
[   88.495363][ T2031]  ? check_panic_on_warn+0x24/0xad
[   88.495633][ T2031]  ? __hlist_bl_del+0xc4/0xd2
[   88.495878][ T2031]  check_panic_on_warn+0x38/0xad
[   88.496138][ T2031]  ? __hlist_bl_del+0xc4/0xd2
[   88.496383][ T2031]  end_report+0xfb/0x116
[   88.496612][ T2031]  kasan_report+0x1a3/0x1b5
[   88.496857][ T2031]  ? __hlist_bl_del+0xc4/0xd2
[   88.497103][ T2031]  __hlist_bl_del+0xc4/0xd2
[   88.497352][ T2031]  ___d_drop+0xb0/0xba
[   88.497568][ T2031]  __d_drop+0x40/0x95
[   88.497778][ T2031]  d_drop+0x22/0x2d
[   88.497979][ T2031]  do_one_tree+0x2b/0x34
[   88.498202][ T2031]  shrink_dcache_for_umount+0x7e/0xfb
[   88.498483][ T2031]  generic_shutdown_super+0x68/0x388
[   88.498758][ T2031]  kill_anon_super+0x3b/0x43
[   88.498997][ T2031]  deactivate_locked_super+0x90/0xd1
[   88.499274][ T2031]  deactivate_super+0xaa/0xb5
[   88.499518][ T2031]  cleanup_mnt+0x103/0x211
[   88.499752][ T2031]  task_work_run+0x12b/0x160
[   88.499760][T22279] ESDFS-fs (esdfs): mounted on top of ./file0 type ext4
[   88.499993][ T2031]  exit_to_user_mode_prepare+0xc4/0x1cb
[   88.500006][ T2031]  syscall_exit_to_user_mode+0x18/0x52
[   88.500918][ T2031]  do_syscall_64+0xa6/0xac
[   88.501150][ T2031]  entry_SYSCALL_64_after_hwframe+0x61/0xcb
[   88.501458][ T2031] RIP: 0033:0x44d50b
[   88.501661][ T2031] Code: 07 00 48 83 c4 08 5b 5d c3 66 0f 1f 44 00 00 c3 66 2e 0f 1f 84 00 00 00 00 00 0f 1f 44 00 00 f3 0f 1e fa b8 a6 00 00 00 0f 05 <48> 3d 00 f0 ff ff 77 05 c3 0f 1f 40 08
[   88.502638][ T2031] RSP: 002b:00007ffcbb7c4b18 EFLAGS: 00000206 ORIG_RAX: 00000000000000a6
[   88.503066][ T2031] RAX: 0000000000000000 RBX: 00007ffcbb7c5e68 RCX: 000000000044d50b
[   88.503468][ T2031] RDX: 0000000000000000 RSI: 000000000000000a RDI: 00007ffcbb7c4bf0
[   88.503884][ T2031] RBP: 00007ffcbb7c5c00 R08: 0000000000000000 R09: 00007ffcbb7c49b0
[   88.504288][ T2031] R10: 00000000023fe88b R11: 0000000000000206 R12: 0000000000000001
[   88.504693][ T2031] R13: 00007ffcbb7c5e58 R14: 00000000004c6770 R15: 0000000000000001
[   88.505098][ T2031]  </TASK>
[   88.505307][ T2031] Kernel Offset: disabled
[   88.505536][ T2031] Rebooting in 86400 seconds..


Vulnerability analysis

The object of uaf is dentry. When esdfs is mounted, it is created in the esdfs_read_super function.
static int esdfs_read_super(struct super_block *sb, const char *dev_name,
		void *raw_data, int silent)
{
	...
	sb->s_root = d_make_root(inode);	 =========> alloc
	...
	d_rehash(sb->s_root);  
	...
}

static void __d_rehash(struct dentry *entry)
{
	struct hlist_bl_head *b = d_hash(entry->d_name.hash); ===========> [1]

	hlist_bl_lock(b);
	hlist_bl_add_head_rcu(&entry->d_hash, b);       ============> add hlist
	hlist_bl_unlock(b);
}

Note [1] here is to calculate hlist_bl_head through entry->d_name.hash.

When the process exits, umount is triggered and shrink_dcache_for_umount() is called.

void shrink_dcache_for_umount(struct super_block *sb)
{
	struct dentry *dentry;

	WARN(down_read_trylock(&sb->s_umount), "s_umount should've been locked");

	dentry = sb->s_root;
	sb->s_root = NULL;
	do_one_tree(dentry);

	while (!hlist_bl_empty(&sb->s_roots)) {
		dentry = dget(hlist_bl_entry(hlist_bl_first(&sb->s_roots), struct dentry, d_hash));
		do_one_tree(dentry);
	}
}

static void do_one_tree(struct dentry *dentry)
{
	shrink_dcache_parent(dentry);
	d_walk(dentry, dentry, umount_check);
	d_drop(dentry);
	dput(dentry);		================> release dentry
}

static void ___d_drop(struct dentry *dentry)
{
	struct hlist_bl_head *b;
	/*
	 * Hashed dentries are normally on the dentry hashtable,
	 * with the exception of those newly allocated by
	 * d_obtain_root, which are always IS_ROOT:
	 */
	if (unlikely(IS_ROOT(dentry)))       ===============> [2]
		b = &dentry->d_sb->s_roots;
	else
		b = d_hash(dentry->d_name.hash);

	hlist_bl_lock(b);
	__hlist_bl_del(&dentry->d_hash);     ===============> del hlist
	hlist_bl_unlock(b);
}
But when dentry is root dentry, the hlist_bl_head used is dentry->d_sb->s_roots, but root dentry actually inserted in dentry->d_name.hash, so hlist_bl_lock does not work, causing the node of hlist to be added
and node deletion can happen at the same time, causing uaf.

## Attachments

- [poc.c](attachments/poc.c) (text/plain, 16.3 KB)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2023-05-11)

[Empty comment from Monorail migration]

### ay...@gmail.com (2023-05-11)

Sorry, I mistakenly submitted a public report at https://bugs.chromium.org/p/chromium/issues/detail?id=1444752, can you help me remove it.

### me...@chromium.org (2023-05-11)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-12)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/282103830). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting  Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/282103830]

### [Deleted User] (2023-05-12)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-23)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-23)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-30)

[Empty comment from Monorail migration]

### ch...@google.com (2023-07-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-14)

Marking this as fixed as per b/282103830

### [Deleted User] (2023-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-14)

[Empty comment from Monorail migration]

### ch...@google.com (2023-07-17)

Marked as started since verification not done yet

### ch...@google.com (2023-07-19)

[Empty comment from Monorail migration]

### ch...@google.com (2023-07-19)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-02)

Congratulations! The VRP Panel has decided to award you $15,000 for this report of kernel memory corruption. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-08-05)

[Empty comment from Monorail migration]

### ay...@gmail.com (2023-09-08)

Thank you very much for the reward, I would like to ask how do I fill in my bank account information for the payment.

### [Deleted User] (2023-10-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-10-25)

This issue was migrated from crbug.com/chromium/1444766?no_tracker_redirect=1

[Monorail blocking: b/282103830]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064508)*
