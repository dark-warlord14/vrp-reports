# Chrome OS exploit: WebAsm, Site Isolation, crosh, crash reporter, cryptohomed

| Field | Value |
|-------|-------|
| **Issue ID** | [40089045](https://issues.chromium.org/issues/40089045) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>JavaScript>WebAssembly, OS>Systems |
| **Platforms** | ChromeOS |
| **Reporter** | gz...@gmail.com |
| **Assignee** | mn...@chromium.org |
| **Created** | 2017-09-18 |
| **Bounty** | $100,000.00 |

## Description

[ WebAsm OOB ArrayBuffer ]

WebAsm instance builder reads imports from an attacker-controlled object in v8/src/wasm/wasm-module.cc:1625 ProcessImports(). Imports can be getters, which run while the instance is being built and is not in a consistent state. If the getter builds another instance for the same module, then the instances will share a WasmCompiledModule, but will have different ArrayBuffers for memory. Compiled module will reference one memory buffer. If the second memory grows, then the compiled module gets confused and relocates to OOB memory. For trunk, the code has moved to wasm/module-compiler.cc. Exploit in wasm_xpl.js.


[ privesc to war-extensions with PageState ]

FrameNavigationEntry (FNE) holds a SiteInstance and PageState. If a FNE is navigated to, then SiteInstance determines the process. PageState can override the URL that the renderer navigates to. content/renderer/render_frame_impl.cc:6250 RFI::NavigateInternal():

  std::unique_ptr<HistoryEntry> entry =
    PageStateToHistoryEntry(request_params.page_state);
  ...
  item_for_history_navigation = entry->root();
  ...
  request = frame_->RequestFromHistoryItem(item_for_history_navigation,
                                           cache_policy);

PageState contains a URL that goes into the request. If the SiteInstance belongs to an extension and the url in PageState shouldn't go to extension process, then the transfer logic kicks in. But data: url is loaded fine. Here's the bug: a frame can overwrite the page_state of any other frame in the same WebContents. Using FrameHostMsg_DidCommitProvisionalLoad, which reaches NCI::RendererDidNavigate() in content/browser/frame_host/navigation_controller_impl.cc:946:

  FrameNavigationEntry* frame_entry =
      active_entry->GetFrameEntry(rfh->frame_tree_node());
  ...
  frame_entry->SetPageState(params.page_state);

FNE is looked up based on frame unique names. A compromised frame can lie about its unique name, and set it to the target extension frame using FrameHostMsg_DidChangeName. But GetFrameEntry only looks for frames in the same WebContents. So an attacker must iframe an extension. This is only possible for the web-accessible-resources. Exploit in index.html and sc.cc.


[ war-extension to crosh with process limit ]

When chrome hits a certain limit of processes, it starts sharing them between renderers. It won't share between extensions and web origins. But it can share between arbitrary extensions. content/browser/renderer_host/render_process_host_impl.cc:3079 RPHI::GetProcessHostForSiteInstance():

  if (!render_process_host &&
      ShouldTryToUseExistingProcessHost(browser_context, site_url)) {
    render_process_host = GetExistingProcessHost(browser_context, site_url);

chrome/browser/extensions/chrome_content_browser_client_extensions_part.cc:398 IsSuitableHost():

  RenderProcessHostPrivilege privilege_required =
      GetPrivilegeRequiredByUrl(site_url, registry);
  return GetProcessPrivilege(process_host, process_map, registry) ==
         privilege_required;

This privilege is coarse grained, basically just PRIV_NORMAL vs PRIV_EXTENSION. The exploit iframes the Image Loader extension which iframes blobs urls to create a bunch of processes. Then it iframes the PDF extension to try and get into crosh extension. It retries until success, then exploits the PDF extension with page state and WebAsm to get control of the crosh extension renderer. Exploit in index.html, rendgen.js and sc.cc.


[ crosh to chronos with awk injection ]

Crosh has access to a limited set of command line commands. network_diag has an awk command injection bug. platform2/crosh/network_diag:382 diag_arp():

  arp="$(${ARP} -an | awk '/('${ip}').*'${ifc}'$/ { print $4 }')"

Run that with ip=.)/{}BEGIN{system(sprintf("echo%c<base64>|base64%c-d|sh",32,32))}#

It uses sprintf %d 32 and base64 for spaces, because crosh splits arguments with spaces. But this awk is actually only reached when the ip belongs to the network of some interface: ip & netmask = network ip. The binary and is done in

do_netmask () {
  local -a ip=($(do_address_parts "$1"))
  local -a mask=($(do_address_parts "$2"))
  local -a ret
  for part in ${!ip[@]}; do
    ret+=("$((ip[part] & mask[part]))")

Which will break if ip[part] is not a number. Surprisingly, bash allows something like $(( a=5 )). And this modifies the variables outside the parenthesis! So craft an ip like this: 192.168.ip[3]=0,8.)/{}BEGIN... That's for the network address 192.168.8.0. It splits into 4 parts. 3rd part is ip[3]=0,8 so it overwrites the garbage in the 4th part to 0 and then evaluates to 8. And now 4th part successfully evaluates as 0! The exploit also uses network_diag to get the actual network address of wlan0. Code in crosher.js.


[ chronos to root with crash reporter and /tmp symlink ]

The crash handler for non-chrome processes copies files to /tmp/crash_reporter/<crashed pid>/ as root. user_collector.cc:130:

  static const char* const kProcFiles[] = {
    "auxv",
    "cmdline",
    "environ",
    "maps",
    "status"
  };
  for (std::string proc_file : kProcFiles) {
    if (!base::CopyFile(process_path.Append(proc_file),
                        container_dir.Append(proc_file))) {

Symlink /tmp/crash_reporter/<getpid()>/environ to /proc/sys/kernel/core_pattern, then crash. And then crash again to launch the command in core_pattern. Actually, this won't work because of protected_symlinks. Even root gets permission denied for non-root symlinks in sticky directories. But surprisingly, this check only seems to apply for a symlink in the last component of a path. So symlink the pid directory to outside the sticky /tmp. And from there, symlink environ to core_pattern. Exploit in crasher.c. There is also a noexec bypass, using bash and dd. See drop/yexec and tools/yesexec.cc.


[ persistence with cryptohomed stateful recovery ]

Cryptohomed has a feature called a stateful recovery. The file /mnt/stateful_partition/decrypt_stateful indicates a recovery request during boot. Cryptohomed takes a username and password hash from decrypt_stateful, decrypts the corresponding cryptohome and copies it to /mnt/stateful_partition/decrypted. And then it reboots. There is probably some sort of recovery USB stick, which asks the user for the password, writes it to decrypt_stateful, boots and later passes the decrypted files to the user. I don't know much about that.

In any case, the copying follows symlinks, so the exploit symlinks modprobe.d source file to /run/modprobe.d and runs a command as root with the uinput module.

There is a race between cryptohomed and uinput. uinput runs after login prompt is visible. With trickery, it's possible to reliably win the race. Chrome depends on the session manager, which reads /var/lib/whitelist/policy during initialization. Turn the policy file into a fifo. Reading of the fifo blocks until something writes to the fifo. Now, symlink then/unblock_session_manager to the fifo. The copying is done breadth first, so unblock_session_manager is written after modprobe.d.

Finally, cryptohomed would reboot, so make it block indefinitely on a then/then/block fifo. Once exploit gets root, it removes decrypt_stateful and restarts cryptohomed. Exploit in drop/persist.


VERSION
Chrome Version: 60.0.3112.114 stable
Operating System: Chrome OS 9592.94.0, Dell Chromebook 11, wolf

REPRODUCTION CASE
* unpack crosxpl2.targ.gz
* run ./webserver
* navigate to http://<ip>:8000/
* wait until a tab opens with lamecalc
* reboot
* lamecalc should open again

gzobqq@gmail.com


## Attachments

- [crosxpl2.tar.gz](attachments/crosxpl2.tar.gz) (application/octet-stream, 5.4 MB)
- [wasm_xpl.js](attachments/wasm_xpl.js) (text/plain, 7.7 KB)
- [index.html](attachments/index.html) (text/plain, 4.9 KB)
- [sc.cc](attachments/sc.cc) (text/plain, 24.0 KB)
- [crosher.js](attachments/crosher.js) (text/plain, 3.2 KB)
- [crasher.c](attachments/crasher.c) (text/plain, 4.2 KB)
- [persist](attachments/persist) (text/plain, 1.6 KB)
- [fix_offsets](attachments/fix_offsets) (text/plain, 1.9 KB)

## Timeline

### me...@chromium.org (2017-09-18)

Thank you for the report! We'll start splitting this into child bugs. Once we can confirm it reproduces, we'll assign a severity.

### me...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### me...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### me...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### me...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### me...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### me...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### ke...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### me...@chromium.org (2017-09-18)

[Comment Deleted]

### mn...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### me...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### mn...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### wf...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### mn...@chromium.org (2017-09-18)

I'll also take ownership of this bug as a point of contact and for overall communication. We have owners for the majority of the steps in the chain already, will make sure we fill in the remaining gaps quickly.

I'll label as Severity-Critical, but P1 since the exploit isn't public. Let's get this sorted quickly, but no reason to spend your nights and weekends on this.

Adding josafat@ as a heads-up: We need a stable respin pretty soon.

### wf...@chromium.org (2017-09-18)

FYI I am handling the reproduction steps now on a wolf device, and will update the bug when I have verified it reproduces.

### aw...@google.com (2017-09-18)

[Empty comment from Monorail migration]

### wf...@chromium.org (2017-09-18)

I successfully reproduced the full chain on:

Platform: 9592.96.0 (Official Build) stable-channel wolf
Firmware: Google_Wolf.4389.24.62
Chrome: 60.0.3112.114 (Official Build) (64-bit)

exploit running as Guest then reboot and persistence is still there in Guest mode.

Critical bugs are p-0 by convention (and should be for our accounting), but I agree with https://crbug.com/chromium/766253#c14 that since this was responsibly disclosed with no evidence of public knowledge there is no need to rush a release here.

### ke...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### me...@chromium.org (2017-09-19)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>WebAssembly OS>Systems]

### sh...@chromium.org (2017-09-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-19)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mn...@chromium.org (2017-09-20)

There's no culprit that introduced this, so nothing to revert and no reason to block beta.

### mn...@chromium.org (2017-09-20)

Note regarding repro: To reproduce in a VM, a slight change to the exploit is needed. VM's don't have wlan0, so you have to substitute wlan0 in crosher.js:70 with eth0.

This is hopefully useful to people verifying fixes.

### cr...@chromium.org (2017-09-22)

mnissler@ or wfh@: Are you able to try repro'ing the exploit on a trunk build of ChromeOS?  I've landed a fix for the PageState priv-esc (https://crbug.com/chromium/766262) in r503297 (63.0.3221.0), and I'd like confirmation that it blocks the exploit before requesting a merge.  (I'm in Tokyo at the moment, and don't have a good way to do it myself.)

Note that you'll probably need to run with --disable-browser-side-navigation on trunk to have a chance of repro'ing it without my fix, since PlzNavigate appears to make the repro steps not work as well.  I'm guessing that means the exploit doesn't work on M61, since PlzNavigate is enabled there via field trial.  (Is that correct?)

Alternatively, you could try patching my fix into an M60 build of ChromeOS to see if it stops the exploit there.  There will be a merge conflict in the browser test, but you can leave that out or use the version of that file from Patchset 2 (https://chromium-review.googlesource.com/c/chromium/src/+/674808/2).

Thanks!

### cr...@chromium.org (2017-09-22)

[Empty comment from Monorail migration]

### mn...@chromium.org (2017-09-22)

[Empty comment from Monorail migration]

### gz...@gmail.com (2017-09-22)

It will be difficult to get the exploit running on trunk. There's just a lot of offsets that are prone to change. See wasm_xpl.js:find_rfi() for example. The last port I did took 12 hours. Porting the fix to M60 is definitely easier, but unfortunately some offsets in the exploit change with recompiled chrome. They're offsets between global objects. I have a script that extracts these from symbolized chrome. But you would have to recompile the shellcode, which unfortunately is messy. I may be able to make a script for you that extracts the offsets from your compiled M60 chrome and patches sc.js.

creis, you are very right about PlzNavigate. See content/renderer/render_frame_impl.cc:6237 in NavigateInternal():

  if (!browser_side_navigation && should_load_request) {
    request = frame_->RequestFromHistoryItem(item_for_history_navigation,

The renderer won't use the url from page state with PlzNavigate. So indeed, the exploit is broken on official M61 with the field trial.

### gz...@gmail.com (2017-09-22)

Here's the script I promised in #27. It patches shellcode to make it run on your compiled 60.0.3112.114. Run in crosxpl2/ as fix_offsets path/to/chrome after each chrome build.

### cr...@chromium.org (2017-09-22)

Thanks!  Glad to hear that both r503297 and PlzNavigate are independently effective (per https://bugs.chromium.org/p/chromium/issues/detail?id=766262#c20).  I'll request merges for the fix.

### mn...@chromium.org (2017-09-25)

Update: We have landed fixes for most links in the exploit chain on ToT, M62, M61. Exceptions are:

* https://crbug.com/chromium/766267 which is technically not a bug that we can quickly fix, but we'll look into adding restrictions to process sharing to mitigate risk.
* the fix for https://crbug.com/chromium/766276 is still missing on M61, merge decision pending.

Suggestions for additional hardening work have come up when analyzing the exploit chain, individual bug owners should file separate issues for that.

Given the above, we are mostly done here. The rollout plan is M61 at this time, which is OK as long as we're not aware of the bugs being actively exploited in the wild.

Thanks everyone for resolving this quickly!

### mn...@chromium.org (2017-10-06)

OK, so we're done here. The Chrome-side changes actually didn't make it into M61, but all Chrome OS side changes did. I'll mark this fixed now, but we should wait to make the bug public only after Chrome OS stable is on 62.

### sh...@chromium.org (2017-10-07)

[Empty comment from Monorail migration]

### as...@chromium.org (2017-10-09)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-10-11)

Many congratulations on the Pwnium reward of $100,000!!!!

### va...@chromium.org (2017-10-11)

i hope it's delivered via absurdly large check :D

### gz...@gmail.com (2017-10-13)

Haha, let's not overdo it :)
But thank you, everyone !!

### aw...@chromium.org (2017-10-14)

[Empty comment from Monorail migration]

### va...@chromium.org (2017-10-31)

[Empty comment from Monorail migration]

### va...@chromium.org (2017-11-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-11-06)

[Empty comment from Monorail migration]

### mn...@chromium.org (2017-11-13)

All done here as we're on 62.

Removing blockers for additional hardening work that strictly isn't part of the response work for this bug and marking public.

### mn...@chromium.org (2017-11-13)

[Empty comment from Monorail migration]

### dc...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### dc...@chromium.org (2018-01-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### is...@google.com (2018-03-27)

This issue was migrated from crbug.com/chromium/766253?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript>WebAssembly, OS>Systems]
[Monorail blocked-on: crbug.com/chromium/766260, crbug.com/chromium/766262, crbug.com/chromium/766271, crbug.com/chromium/766275, crbug.com/chromium/766276]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089045)*
