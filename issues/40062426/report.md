# [ChromeOS Security] Multiple Share Memory TOCTOU Vulnerabilities in Qualcomm Snapdragon 7c Gen 2 Camera Drivers Which can be triggered from Chome Browser Context

| Field | Value |
|-------|-------|
| **Issue ID** | [40062426](https://issues.chromium.org/issues/40062426) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | OS>Packages |
| **Platforms** | ChromeOS |
| **Reporter** | pi...@gmail.com |
| **Assignee** | ri...@google.com |
| **Created** | 2022-12-29 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

Backgroud:

My test chromebook is lenovo chromebook duet3, which is Qualcomm Snapdragon 7c Gen 2 Compute Platform according to Google result. The Kernel version is 5.4

On duet3, the camera drivers are Qualcomm's camx:

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:/src/third_party/kernel/v5.4/drivers/media/platform/camx/>

From the device nodes view, they are video nodes and v4l-subdev nodes:  

/dev/video\* /dev/v4l-subdev\*

localhost ~ # ls -lZ /dev/video1  

crw-rw----. 1 root video u:object\_r:device:s0 81, 1 Dec 28 20:09 /dev/video1  

localhost ~ # ls -lZ /dev/v4l-subdev7  

crw-rw----. 1 root video u:object\_r:device:s0 81, 9 Dec 28 20:09 /dev/v4l-subdev7

These device nodes can be accessed by chrome browser context, means user chronos + u:r:cros\_browser:s0 can access this drivers, crosh app can access them also.

The /dev/video1 on duet3 is exposed by cam\_req\_mgr driver, its ioctl function is cam\_private\_ioctl:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.4/drivers/media/platform/camx/cam_req_mgr/cam_req_mgr_dev.c;drc=2b56f86e4cf88bd32a63d7eb6b29df8c7f530921;l=218>

cam\_req\_mgr is a central driver which responsible for v4l-subdev drivers request / memory / handle management.

The /dev/v4l-subdev\* are subdevs like cam-isp, cam-jpeg etc, some of the subdev drivers share a common ioctl function cam\_node\_handle\_ioctl:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.4/drivers/media/platform/camx/cam_core/cam_node.c;drc=9e50f9c768e6a9e3298b1031569a2f32a10bb5ec;l=667>

The Bugs:

When these drivers works together, there is memory or buf\_handle management in cam\_req\_mgr, cam\_req\_mgr can map and allocate dmabuf memory which can be mapped both in userspace and kernel address space, works like a share memory between userspace and drivers

For example, CAM\_REQ\_MGR\_ALLOC\_BUF ioctl cmd of cam\_req\_mgr can allocate and map dmabuf to kernel address space and return the dmabuf fd to userspace, so userspace can mmap the fd to its address space.  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.4/drivers/media/platform/camx/cam_req_mgr/cam_req_mgr_dev.c;drc=2b56f86e4cf88bd32a63d7eb6b29df8c7f530921;l=379>

Besides the dmabuf fd, there is also a buf\_handle passed to userspace,when input buf\_handle to subdevs ioctl cmd handler, it can find the dmabuf kernel address from the buf\_handle by using function cam\_mem\_get\_cpu\_buf:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.4/drivers/media/platform/camx/cam_req_mgr/cam_mem_mgr.c;drc=4ab54ae95f4a2496048ec88ac36168f724d45636;l=175>

```
idx = CAM_MEM_MGR_GET_HDL_IDX(buf_handle);   <-------- get idx from input buf_handle  
if (idx >= CAM_MEM_BUFQ_MAX || idx <= 0)  
	return -EINVAL;  

//skip...  

\*vaddr_ptr = tbl.bufq[idx].kmdvaddr;   <---------- get the kernel va of the dmabuf, tbl is a global table  
\*len = tbl.bufq[idx].len;           <-------- get the len of dmabuf mapping  

```

So after call cam\_mem\_get\_cpu\_buf, drivers can get the dmabuf kernel va and len, then can get the share memory content to process, before use these share memory content, drivers will validate them to avoide memory corruption bugs.

But drivers don't copy the share memory before use it, so there are TOCTOU bugs.

By just search cam\_mem\_get\_cpu\_buf in the drivers code, you can get many examples like oob write and read.

For example in function cam\_eeprom\_get\_cal\_data:  

static int32\_t cam\_eeprom\_get\_cal\_data(struct cam\_eeprom\_ctrl\_t \*e\_ctrl,  

struct cam\_packet \*csl\_packet)  

{  

//skip...

```
io_cfg = (struct cam_buf_io_cfg \*) ((uint8_t \*)  
	&csl_packet->payload +  
	csl_packet->io_configs_offset);     <--- csl_packet is a shm pointer which from cam_mem_get_cpu_buf in outside function  

for (i = 0; i < csl_packet->num_io_configs; i++) {  
	CAM_DBG(CAM_EEPROM, "Direction: %d:", io_cfg->direction);  
	if (io_cfg->direction == CAM_BUF_OUTPUT) {  
		rc = cam_mem_get_cpu_buf(io_cfg->mem_handle[0],  
			&buf_addr, &buf_size);            <------------ get the kernel va  
		if (rc) {  
			CAM_ERR(CAM_EEPROM, "Fail in get buffer: %d",  
				rc);  
			return rc;  
		}  
		if (buf_size <= io_cfg->offsets[0]) {              <---------- check bounds, io_cfg is in share memory  
			CAM_ERR(CAM_EEPROM, "Not enough buffer");  
			rc = -EINVAL;  
			goto rel_cmd_buf;  
		}  

		remain_len = buf_size - io_cfg->offsets[0];  
		CAM_DBG(CAM_EEPROM, "buf_addr : %pK, buf_size : %zu\n",  
			(void \*)buf_addr, buf_size);  

		read_buffer = (uint8_t \*)buf_addr;         <-------- assign to read_buffer  
		if (!read_buffer) {  
			CAM_ERR(CAM_EEPROM,  
				"invalid buffer to copy data");  
			rc = -EINVAL;  
			goto rel_cmd_buf;  
		}  
		read_buffer += io_cfg->offsets[0];         <-------- offset TOCTOU, add offset to the kernel va  

		if (remain_len < e_ctrl->cal_data.num_data) {  
			CAM_ERR(CAM_EEPROM,  
				"failed to copy, Invalid size");  
			rc = -EINVAL;  
			goto rel_cmd_buf;  
		}  

		CAM_DBG(CAM_EEPROM, "copy the data, len:%d",  
			e_ctrl->cal_data.num_data);  
		memcpy(read_buffer, e_ctrl->cal_data.mapdata,    <------ memcpy to the kernel va + offset, oob write  
				e_ctrl->cal_data.num_data);  
    
         //skip.....  

```

}

Another simple example:  

int cam\_packet\_util\_process\_patches(struct cam\_packet \*packet,  

int32\_t iommu\_hdl, int32\_t sec\_mmu\_hdl, int pf\_dump\_flag)  

{

```
/\* process patch descriptor \*/  
patch_desc = (struct cam_patch_desc \*)  
		((uint32_t \*) &packet->payload +  
		packet->patch_offset/4);    <-------- patch_offset is checked in outside function, can TOCTOU here  

    //skip...  

```

}

Bypass Driver Occupy Mechanism:

Because /dev/video1 is exposed by cam\_req\_mgr, but in its open function cam\_req\_mgr\_open, there is a occupy design, only allow one process open it:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.4/drivers/media/platform/camx/cam_req_mgr/cam_req_mgr_dev.c;drc=2b56f86e4cf88bd32a63d7eb6b29df8c7f530921;l=111>

/dev/video1 is opened by /usr/bin/cros\_camera\_service, chronos user with u:r:cros\_browser:s0 can't directly kill the cros\_camera\_service process. So needs a method to bypass this occupy mechanism.

By investigate the cros\_camera\_service code, I saw there is a process quit mechanism in handling mojo channel error, function CameraHalServerImpl::IPCBridge::OnServiceMojoChannelError:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform2/camera/hal_adapter/camera_hal_server_impl.cc;drc=00a9db7f171e353f24ea5adba89b4bd5ee549116;l=244>

So this means, chrome browser itself can trigger the cros\_camera\_service to quit and occupy the /dev/video1 fd.

For convenience of testing, I just kill the chrome browser process before running the poc in the chronos shell.

**VERSION**

chromium os kernel v5.4 latest code of camx, tested on lenovo chromebook duet3

**REPRODUCTION CASE**

I wrote a PoC which will trigger above cam\_packet\_util\_process\_patches patch\_offset TOCTOU, there is thread function called race to change patch\_offset continuelly.

It crahsed my duet3 kernel.

You can see the readme.txt to know how to reproduce.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

chromebook kernel crash, see attachment

**CREDIT INFORMATION**

Reporter credit: [lovepink]

## Attachments

- [cros_cam_dmabuf_shm_toctou.zip](attachments/cros_cam_dmabuf_shm_toctou.zip) (application/octet-stream, 1.5 MB)

## Timeline

### [Deleted User] (2022-12-29)

[Empty comment from Monorail migration]

### li...@chromium.org (2022-12-29)

Sending to Chrome OS security for triage.

### en...@google.com (2022-12-29)

Thanks for the thorough report lovepink, could you provide the ChromeOS version: first line from chrome://version

_______________________________________________________________

Assigning to jcliang@ based on code change history. CC'ing other relevant parties.
Setting severity to high based on dma involvement. Note: This might classify as an upstream bug!

[Monorail components: OS>Packages]

### pi...@gmail.com (2022-12-30)

Hi,
I finally manage to update my duet3 to latest stable recovery images according to https://chromiumdash.appspot.com/serving-builds?deviceCategory=ChromeOS , so please ignore above comments which I have deleted.

On the 107 stable version, my PoCs still work, but the browser process kill name is different so I update the reproduce steps in readme.txt here:

Run the poc like below, kill the chrome process and quickly run the poc:

localhost /usr/local # chmod +x cros_cam_jpeg_race
localhost /usr/local # su chronos
chronos@localhost /usr/local $ kill -9 `ps -ef | grep "/opt/google/chrome/chrome --enable-native-gpu-memory-buffers" | grep -v grep | awk '{print $2}'`
chronos@localhost /usr/local $ ./cros_cam_jpeg_race

### pi...@gmail.com (2022-12-30)

My duet3 auto updated to 108 stable version, https://crbug.com/chromium/1404039#c4 reproduce steps still work.

### pi...@gmail.com (2022-12-30)

After updated to 108 stable version, the duet3 kernel version is v5.15 now, the vulnerable codes are still the same, for example cam_mem_get_cpu_buf still return the kernel share memory address but not copy out the share content:
https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/media/platform/camx/cam_req_mgr/cam_mem_mgr.c;drc=f133a061e1ae1a880a567c4c7e7066e1eeedead3;l=178
And the caller of cam_mem_get_cpu_buf , also directly use the share memory address also not copy out the share content which cause TOCTOU, for exmaple:
https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.15/drivers/media/platform/camx/cam_core/cam_context_utils.c;drc=b5b062f1100066d2d07b8f2c34a6bcd7292ccade;l=381

### pi...@gmail.com (2022-12-30)

chrome://versions picture I posted here: https://bugs.chromium.org/p/chromium/issues/detail?id=1404036#c13

### jc...@google.com (2022-12-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-12)

hywu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ri...@google.com (2023-01-23)

The vendor has been notified and they are working on a fix. It is going through their internal review process and hopefully we can merge it into ChromeOS soon.

Also it seems that an attacker needs to either control the ChromeOS process, the camera HAL, or be in dev mode, luckily that limits the severity of the bug. Will keep you posted with any update.

Thank a lot for the detailed report

### [Deleted User] (2023-01-27)

hywu: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tf...@chromium.org (2023-01-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-28)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ri...@google.com (2023-03-13)

Reducing prio after landing mitigations b/266181515

### [Deleted User] (2023-03-13)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ri...@google.com (2023-05-01)

Fixed at b/264148881

### ri...@google.com (2023-05-01)

[Empty comment from Monorail migration]

### pi...@gmail.com (2023-05-02)

Hi, just see these issues got fixed, will this report get reward? Thanks

### ch...@google.com (2023-05-02)

The reward panel will check this report soon and decide on reward

### [Deleted User] (2023-05-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-02)

[Empty comment from Monorail migration]

### ro...@google.com (2023-05-09)

[Empty comment from Monorail migration]

### ro...@google.com (2023-05-09)

Note this was modified to an S2 in Buganizer but not updated here. The reason for lowering the severity is in https://crbug.com/chromium/1404039#c10 above. 

### am...@google.com (2023-05-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-19)

Congratulations on yet another one, lovepink! The VRP Panel has decided to award you $10,000 for this report of a mildly mitigated security bug resulting in the potential for memory corruption in the browser process of ChromeOS. Thank you for your efforts and reporting this issue to us! 

### am...@chromium.org (2023-05-22)

reward info sent to finance for processing on Friday, 19 May; automation did not update this issue correctly

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-08-08)

This issue was migrated from crbug.com/chromium/1404039?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062426)*
