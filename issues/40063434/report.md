# Security: Race Condition UAF in evdi_painter_mode_changed_notify

| Field | Value |
|-------|-------|
| **Issue ID** | [40063434](https://issues.chromium.org/issues/40063434) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | lm...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2023-03-07 |
| **Bounty** | $6,000.00 |

## Description

**VULNERABILITY DETAILS**

ioctl$EVDI\_CONNECT will call \*evdi\_painter\_connect\_ioctl\* to connect/disconnect painter. if \*cmd->connected\* is false, evdi\_painter\_disconnect will be called. \*painter->scanout\_fb\* will be put[1] under \*painter->lock\*, that is fine. But \*evdi\_painter\_mode\_changed\_notify\* will access \*painter->scanout\_fb->base\* without \*painter->lock\* locked, there may be a race condition UAF[3].

```
static int evdi_painter_disconnect(struct evdi_device \*evdi,  
        struct drm_file \*file)  
{  
        struct evdi_painter \*painter = evdi->painter;  
        char buf[100];  
  
        EVDI_CHECKPT();  
  
        painter_lock(painter);  
  
        if (file != painter->drm_filp) {  
                painter_unlock(painter);  
                return -EFAULT;  
        }  
  
        if (painter->scanout_fb) {  
                drm_framebuffer_put(&painter->scanout_fb->base);        // [1]  
                painter->scanout_fb = NULL;  
        }  
  
        ......  
}  
  
void evdi_painter_mode_changed_notify(struct evdi_device \*evdi,  
                                      struct drm_display_mode \*new_mode)  
{  
        struct evdi_painter \*painter = evdi->painter;  
        struct drm_framebuffer \*fb;  
        int bits_per_pixel;  
        uint32_t pixel_format;  
        char buf[100];  
  
        if (painter == NULL)  
                return;  
  
        fb = &painter->scanout_fb->base;            // [2]  
        if (fb == NULL)  
                return;  
  
        bits_per_pixel = fb->format->cpp[0] \* 8;    // [3]  
        pixel_format = fb->format->format;  
  
  
        evdi_log_pixel_format(pixel_format, buf, sizeof(buf));  
        EVDI_INFO("(card%d) Notifying mode changed: %dx%d@%d; bpp %d; %s",  
                   evdi->dev_index, new_mode->hdisplay, new_mode->vdisplay,  
                   drm_mode_vrefresh(new_mode), bits_per_pixel, buf);  
  
        evdi_painter_send_mode_changed(painter,  
                                       new_mode,  
                                       bits_per_pixel,  
                                       pixel_format);  
        painter->needs_full_modeset = false;  
}  
  

```

evdi\_painter\_disconnect | evdi\_painter\_mode\_changed\_notify  

painter\_unlock | fb = &painter->scanout\_fb->base; [2]  

drm\_framebuffer\_put [1] |  

| bits\_per\_pixel = fb->format->cpp[0] \* 8; [3] <---------UAF

[1] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.10/drivers/gpu/drm/evdi/evdi_painter.c;drc=2a20b22cd107d774fb72ca50660ce11b9d5ef22b;l=912>  

[2] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.10/drivers/gpu/drm/evdi/evdi_painter.c;drc=2a20b22cd107d774fb72ca50660ce11b9d5ef22b;l=741>  

[3] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.10/drivers/gpu/drm/evdi/evdi_painter.c;drc=2a20b22cd107d774fb72ca50660ce11b9d5ef22b;l=745>

**VERSION**  

Operating System: ChromiumOS Kernel 5.10 stable + dev

**REPRODUCTION CASE**  

This issue is discovered by manual code review, I will try to construct a poc to reproduce it.

BISECT  

<https://source.chromium.org/chromiumos/_/chromium/chromiumos/third_party/kernel/+/3e21cedd503fabd195cf407652bf87fd83e202ac>

FIX PATCH SUGGESTION  

I think the follwing patch should fix the problem.

```
diff --git a/drivers/gpu/drm/evdi/evdi_painter.c b/drivers/gpu/drm/evdi/evdi_painter.c  
index 8e70f495111a..f390bf11a706 100644  
--- a/drivers/gpu/drm/evdi/evdi_painter.c  
+++ b/drivers/gpu/drm/evdi/evdi_painter.c  
@@ -738,13 +738,18 @@ void evdi_painter_mode_changed_notify(struct evdi_device \*evdi,  
        if (painter == NULL)  
                return;  
   
+       painter_lock(painter);  
        fb = &painter->scanout_fb->base;  
        if (fb == NULL)  
+       {  
+               painter_unlock(painter);  
                return;  
+       }  
   
        bits_per_pixel = fb->format->cpp[0] \* 8;  
        pixel_format = fb->format->format;  
   
+       painter_unlock(painter);  
   
        evdi_log_pixel_format(pixel_format, buf, sizeof(buf));  
        EVDI_INFO("(card%d) Notifying mode changed: %dx%d@%d; bpp %d; %s",  

```

## Attachments

- [poc.tar](attachments/poc.tar) (application/octet-stream, 40.0 KB)

## Timeline

### [Deleted User] (2023-03-07)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-03-08)

[Empty comment from Monorail migration]

### en...@google.com (2023-03-09)

Might need to be reported upstream. CC'ing robdclark@ to confirm.

### ro...@chromium.org (2023-03-09)

evdi is downstream displaylink driver

### en...@google.com (2023-03-09)

[Empty comment from Monorail migration]

### gr...@chromium.org (2023-03-09)

Can we get someone from Synaptics involved ?

### en...@google.com (2023-03-10)

[Empty comment from Monorail migration]

### en...@google.com (2023-03-10)

I can also add people from displaylink if needed.

### lu...@synaptics.com (2023-03-13)

Nice, We will take a look on it.

### lu...@synaptics.com (2023-03-13)

Suggested fix is fine. I will prepare fixes chromiumos kernels.

### en...@google.com (2023-03-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-14)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### lm...@gmail.com (2023-03-15)

Impressive response time. I wrote a connect/disconnect poc using evdi_lib, but didn't know how to trigger crtc event. Could you give me some suggestions?

### ha...@google.com (2023-03-21)

Assigning this to rob, so we have an owner. Let's continue collaborating

### lu...@synaptics.com (2023-03-21)

The proposed fix is fine. It is working for me on CrOS and Linux.

However I am not sure if it is feasable to use that vulnerability as to do it you have to do what compositor is doing, and this is only possible when you are have drm master of the device.
Usually system compositor like xserver/wayland/Chrome has drm master so malicious app have to do it before system compositor will attempt to open evdi device. If i recall corectly you need root as well to get open device as drm master.


### lu...@synaptics.com (2023-03-21)

Personally this blog entry was usefull to me to have a grasp to understand how to use linux drm devices.
https://dvdhrm.wordpress.com/2012/09/13/linux-drm-mode-setting-api/ 
You can inspire with it to write poc.

### lm...@gmail.com (2023-03-22)

Hello, Thank you for your sharing, I will try it.

re: https://crbug.com/chromium/1422250#c16, this issue may be used as part of a full-chain exploits. For example, if chrome is compromised, then we can use this issue to escape sandbox/privilege escape.


### [Deleted User] (2023-03-24)

robdclark: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-24)

[Empty comment from Monorail migration]

### lu...@synaptics.com (2023-03-27)

I am validating and preparing patches for this.

### lu...@synaptics.com (2023-03-27)

I have raised issue in partner issue tracker:
https://partnerissuetracker.corp.google.com/issues/275231046

### lu...@synaptics.com (2023-03-28)

Hi Rob, groeck 
Please review.

This was applied to 4.4, 4.14, 4.19, 5.4, 5.10 and 5.15 kernels here:
https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4373672
https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4373674
https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377238
https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377240 
https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377242
https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377244


### gi...@appspot.gserviceaccount.com (2023-03-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/6741e7a617ed12250ceb7a095a30257044998730

commit 6741e7a617ed12250ceb7a095a30257044998730
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Mon Mar 13 13:44:52 2023

CHROMIUM: dlm/evdi: Guard access to painter scanout_fb with painter mutex

BUG=b:275231046,chromium:1422250
TEST=Tested on drallion,grunt,soraka

Change-Id: I2894e99d308530f2831a4fa46f347e5492906195
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377238
Commit-Queue: Guenter Roeck <groeck@chromium.org>
Reviewed-by: Guenter Roeck <groeck@chromium.org>
Tested-by: Guenter Roeck <groeck@chromium.org>

[modify] https://crrev.com/6741e7a617ed12250ceb7a095a30257044998730/drivers/gpu/drm/evdi/evdi_painter.c


### gi...@appspot.gserviceaccount.com (2023-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/49af986f96f92f513ff3548af3fc81d4b943a510

commit 49af986f96f92f513ff3548af3fc81d4b943a510
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Mon Mar 13 13:30:30 2023

CHROMIUM: dlm/evdi: Guard access to painter scanout_fb with painter mutex

BUG=b:275231046,chromium:1422250
TEST=Tested on drallion,grunt,soraka

Change-Id: I32a4c71da53eeb49e56d7a28f42ecd8f3e613e43
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377244
Reviewed-by: Guenter Roeck <groeck@chromium.org>
Commit-Queue: Guenter Roeck <groeck@chromium.org>
Tested-by: Guenter Roeck <groeck@chromium.org>

[modify] https://crrev.com/49af986f96f92f513ff3548af3fc81d4b943a510/drivers/gpu/drm/evdi/evdi_painter.c


### gi...@appspot.gserviceaccount.com (2023-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/eeca5426a7ad04f2d9ba15419df433705a452814

commit eeca5426a7ad04f2d9ba15419df433705a452814
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Mon Mar 13 13:30:30 2023

CHROMIUM: dlm/evdi: Guard access to painter scanout_fb with painter mutex

BUG=b:275231046,chromium:1422250
TEST=Tested on drallion,grunt,soraka

Change-Id: I32a4c71da53eeb49e56d7a28f42ecd8f3e613e43
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377242
Reviewed-by: Guenter Roeck <groeck@chromium.org>
Commit-Queue: Guenter Roeck <groeck@chromium.org>
Tested-by: Guenter Roeck <groeck@chromium.org>

[modify] https://crrev.com/eeca5426a7ad04f2d9ba15419df433705a452814/drivers/gpu/drm/evdi/evdi_painter.c


### gi...@appspot.gserviceaccount.com (2023-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/49af986f96f92f513ff3548af3fc81d4b943a510

commit 49af986f96f92f513ff3548af3fc81d4b943a510
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Mon Mar 13 13:30:30 2023

CHROMIUM: dlm/evdi: Guard access to painter scanout_fb with painter mutex

BUG=b:275231046,chromium:1422250
TEST=Tested on drallion,grunt,soraka

Change-Id: I32a4c71da53eeb49e56d7a28f42ecd8f3e613e43
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377244
Reviewed-by: Guenter Roeck <groeck@chromium.org>
Commit-Queue: Guenter Roeck <groeck@chromium.org>
Tested-by: Guenter Roeck <groeck@chromium.org>

[modify] https://crrev.com/49af986f96f92f513ff3548af3fc81d4b943a510/drivers/gpu/drm/evdi/evdi_painter.c


### gi...@appspot.gserviceaccount.com (2023-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/d337ac22e1150415cbfad9020df97966af60c604

commit d337ac22e1150415cbfad9020df97966af60c604
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Mon Mar 13 13:44:52 2023

CHROMIUM: dlm/evdi: Guard access to painter scanout_fb with painter mutex

BUG=b:275231046,chromium:1422250
TEST=Tested on drallion,grunt,soraka

Change-Id: I2894e99d308530f2831a4fa46f347e5492906195
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377240
Tested-by: Guenter Roeck <groeck@chromium.org>
Reviewed-by: Guenter Roeck <groeck@chromium.org>
Commit-Queue: Guenter Roeck <groeck@chromium.org>

[modify] https://crrev.com/d337ac22e1150415cbfad9020df97966af60c604/drivers/gpu/drm/evdi/evdi_painter.c


### gi...@appspot.gserviceaccount.com (2023-04-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/7c6367d9198ec0322d0cb29189029119a8474897

commit 7c6367d9198ec0322d0cb29189029119a8474897
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Mon Mar 13 13:44:52 2023

CHROMIUM: dlm/evdi: Guard access to painter scanout_fb with painter mutex

BUG=b:275231046,chromium:1422250
TEST=Tested on drallion,grunt,soraka

Change-Id: I2894e99d308530f2831a4fa46f347e5492906195
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4373674
Tested-by: Guenter Roeck <groeck@chromium.org>
Reviewed-by: Guenter Roeck <groeck@chromium.org>

[modify] https://crrev.com/7c6367d9198ec0322d0cb29189029119a8474897/drivers/gpu/drm/evdi/evdi_painter.c


### gi...@appspot.gserviceaccount.com (2023-04-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/a6e385116edd6ec6a833969e7f46fab6992e01f3

commit a6e385116edd6ec6a833969e7f46fab6992e01f3
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Mon Mar 13 13:30:30 2023

CHROMIUM: dlm/evdi: Guard access to painter scanout_fb with painter mutex

BUG=b:275231046,chromium:1422250
TEST=Tested on drallion,grunt,soraka
UPSTREAM-TASK=b:275777499

Change-Id: Id1cce6393d6adaa8b65f36fbfd475b6e5e68e4fb
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377244
Reviewed-by: Guenter Roeck <groeck@chromium.org>
Commit-Queue: Guenter Roeck <groeck@chromium.org>
Tested-by: Guenter Roeck <groeck@chromium.org>
(cherry picked from commit 49af986f96f92f513ff3548af3fc81d4b943a510)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4384505

[modify] https://crrev.com/a6e385116edd6ec6a833969e7f46fab6992e01f3/drivers/gpu/drm/evdi/evdi_painter.c


### gi...@appspot.gserviceaccount.com (2023-04-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/2e551eb922cdcab6714256bdea27e6fcc13e3936

commit 2e551eb922cdcab6714256bdea27e6fcc13e3936
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Mon Mar 13 13:30:30 2023

CHROMIUM: dlm/evdi: Guard access to painter scanout_fb with painter mutex

BUG=b:275231046,chromium:1422250
TEST=Tested on drallion,grunt,soraka
UPSTREAM-TASK=b:275777499

Change-Id: Ieba12e246f3fe24b27d23135f1dc86f55839f84e
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377242
Reviewed-by: Guenter Roeck <groeck@chromium.org>
Commit-Queue: Guenter Roeck <groeck@chromium.org>
Tested-by: Guenter Roeck <groeck@chromium.org>
(cherry picked from commit eeca5426a7ad04f2d9ba15419df433705a452814)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4384223

[modify] https://crrev.com/2e551eb922cdcab6714256bdea27e6fcc13e3936/drivers/gpu/drm/evdi/evdi_painter.c


### gi...@appspot.gserviceaccount.com (2023-04-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/9d4299fb28f5d326875dc0daf1f5e836deea431f

commit 9d4299fb28f5d326875dc0daf1f5e836deea431f
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Mon Mar 13 13:44:52 2023

CHROMIUM: dlm/evdi: Guard access to painter scanout_fb with painter mutex

BUG=b:275231046,chromium:1422250
TEST=Tested on drallion,grunt,soraka
UPSTREAM-TASK=b:275777499

Change-Id: I485edcad02b4e1604a25fe402ae7cd8bc312189b
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4373674
Tested-by: Guenter Roeck <groeck@chromium.org>
Reviewed-by: Guenter Roeck <groeck@chromium.org>
(cherry picked from commit 7c6367d9198ec0322d0cb29189029119a8474897)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4392566
Commit-Queue: Guenter Roeck <groeck@chromium.org>

[modify] https://crrev.com/9d4299fb28f5d326875dc0daf1f5e836deea431f/drivers/gpu/drm/evdi/evdi_painter.c


### gi...@appspot.gserviceaccount.com (2023-04-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/4ed1c55f99629ba54a02b6e6a3c7fccc2e60b38b

commit 4ed1c55f99629ba54a02b6e6a3c7fccc2e60b38b
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Mon Mar 13 13:44:52 2023

CHROMIUM: dlm/evdi: Guard access to painter scanout_fb with painter mutex

BUG=b:275231046,chromium:1422250
TEST=Tested on drallion,grunt,soraka
UPSTREAM-TASK=b:275777499

Change-Id: I178f9f114d72642f7d5b88c066d20d4d035e4ada
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377238
Commit-Queue: Guenter Roeck <groeck@chromium.org>
Reviewed-by: Guenter Roeck <groeck@chromium.org>
Tested-by: Guenter Roeck <groeck@chromium.org>
(cherry picked from commit 6741e7a617ed12250ceb7a095a30257044998730)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4384219

[modify] https://crrev.com/4ed1c55f99629ba54a02b6e6a3c7fccc2e60b38b/drivers/gpu/drm/evdi/evdi_painter.c


### gi...@appspot.gserviceaccount.com (2023-04-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/8f01a17b8a7631119ed5d24a2973ad23783cd47b

commit 8f01a17b8a7631119ed5d24a2973ad23783cd47b
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Mon Mar 13 13:44:52 2023

CHROMIUM: dlm/evdi: Guard access to painter scanout_fb with painter mutex

BUG=b:275231046,chromium:1422250
TEST=Tested on drallion,grunt,soraka
UPSTREAM-TASK=b:275777499

Change-Id: I902a82ca6d29253212e4905ac89b3a513cf4b043
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377240
Tested-by: Guenter Roeck <groeck@chromium.org>
Reviewed-by: Guenter Roeck <groeck@chromium.org>
Commit-Queue: Guenter Roeck <groeck@chromium.org>
(cherry picked from commit d337ac22e1150415cbfad9020df97966af60c604)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4384221

[modify] https://crrev.com/8f01a17b8a7631119ed5d24a2973ad23783cd47b/drivers/gpu/drm/evdi/evdi_painter.c


### gi...@appspot.gserviceaccount.com (2023-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/16a6f010be5589debdf202adadda3f63d09b6422

commit 16a6f010be5589debdf202adadda3f63d09b6422
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Mon Mar 13 13:44:52 2023

CHROMIUM: dlm/evdi: Guard access to painter scanout_fb with painter mutex

BUG=b:275231046,chromium:1422250
TEST=Tested on drallion,grunt,soraka
UPSTREAM-TASK=b:275748736

Change-Id: I5ce4db748275f06bd45ea172f0600c76ed9c6971
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4373674
Tested-by: Guenter Roeck <groeck@chromium.org>
Reviewed-by: Guenter Roeck <groeck@chromium.org>
(cherry picked from commit 7c6367d9198ec0322d0cb29189029119a8474897)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4392568
Commit-Queue: Guenter Roeck <groeck@chromium.org>

[modify] https://crrev.com/16a6f010be5589debdf202adadda3f63d09b6422/drivers/gpu/drm/evdi/evdi_painter.c


### gi...@appspot.gserviceaccount.com (2023-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/c370f8f9dae08c3e2fec7c01105036b5b9313d0f

commit c370f8f9dae08c3e2fec7c01105036b5b9313d0f
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Mon Mar 13 13:30:30 2023

CHROMIUM: dlm/evdi: Guard access to painter scanout_fb with painter mutex

BUG=b:275231046,chromium:1422250
TEST=Tested on drallion,grunt,soraka
UPSTREAM-TASK=b:275748736

Change-Id: I73bc85a51809fb70124436879ebd4da06ce9e177
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377242
Reviewed-by: Guenter Roeck <groeck@chromium.org>
Commit-Queue: Guenter Roeck <groeck@chromium.org>
Tested-by: Guenter Roeck <groeck@chromium.org>
(cherry picked from commit eeca5426a7ad04f2d9ba15419df433705a452814)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4384214

[modify] https://crrev.com/c370f8f9dae08c3e2fec7c01105036b5b9313d0f/drivers/gpu/drm/evdi/evdi_painter.c


### gi...@appspot.gserviceaccount.com (2023-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/96058357ecea63954fe9cc2d1584c18003fb4d3a

commit 96058357ecea63954fe9cc2d1584c18003fb4d3a
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Mon Mar 13 13:30:30 2023

CHROMIUM: dlm/evdi: Guard access to painter scanout_fb with painter mutex

BUG=b:275231046,chromium:1422250
TEST=Tested on drallion,grunt,soraka
UPSTREAM-TASK=b:275748736

Change-Id: Ia6133f05782d79cf5d8e3bb7b2f0b5152c29d2f0
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377244
Reviewed-by: Guenter Roeck <groeck@chromium.org>
Commit-Queue: Guenter Roeck <groeck@chromium.org>
Tested-by: Guenter Roeck <groeck@chromium.org>
(cherry picked from commit 49af986f96f92f513ff3548af3fc81d4b943a510)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4384216

[modify] https://crrev.com/96058357ecea63954fe9cc2d1584c18003fb4d3a/drivers/gpu/drm/evdi/evdi_painter.c


### gi...@appspot.gserviceaccount.com (2023-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/874d29c92057cf76050b2285710625ef86da91df

commit 874d29c92057cf76050b2285710625ef86da91df
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Mon Mar 13 13:44:52 2023

CHROMIUM: dlm/evdi: Guard access to painter scanout_fb with painter mutex

BUG=b:275231046,chromium:1422250
TEST=Tested on drallion,grunt,soraka
UPSTREAM-TASK=b:275748736

Change-Id: I616bfa6b3baf79ead1c64ecc88ef7599456e6808
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377238
Commit-Queue: Guenter Roeck <groeck@chromium.org>
Reviewed-by: Guenter Roeck <groeck@chromium.org>
Tested-by: Guenter Roeck <groeck@chromium.org>
(cherry picked from commit 6741e7a617ed12250ceb7a095a30257044998730)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4384210

[modify] https://crrev.com/874d29c92057cf76050b2285710625ef86da91df/drivers/gpu/drm/evdi/evdi_painter.c


### gi...@appspot.gserviceaccount.com (2023-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/6511ed3d9bc7ecd813d0bea504f7496e2bce8d60

commit 6511ed3d9bc7ecd813d0bea504f7496e2bce8d60
Author: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Date: Mon Mar 13 13:44:52 2023

CHROMIUM: dlm/evdi: Guard access to painter scanout_fb with painter mutex

BUG=b:275231046,chromium:1422250
TEST=Tested on drallion,grunt,soraka
UPSTREAM-TASK=b:275748736

Change-Id: Id7c44af678e833dfc7aa55bba6a3536799acf38d
Signed-off-by: Łukasz Spintzyk <lukasz.spintzyk@synaptics.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4377240
Tested-by: Guenter Roeck <groeck@chromium.org>
Reviewed-by: Guenter Roeck <groeck@chromium.org>
Commit-Queue: Guenter Roeck <groeck@chromium.org>
(cherry picked from commit d337ac22e1150415cbfad9020df97966af60c604)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4384212

[modify] https://crrev.com/6511ed3d9bc7ecd813d0bea504f7496e2bce8d60/drivers/gpu/drm/evdi/evdi_painter.c


### [Deleted User] (2023-04-08)

robdclark: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### lu...@synaptics.com (2023-04-11)

This is fixed, and backported to R112, R113. To be closed

### gr...@chromium.org (2023-04-11)

Marking Fixed as per #41

### [Deleted User] (2023-04-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-12)

[Empty comment from Monorail migration]

### pa...@chromium.org (2023-04-25)

Re: #18, I think the attack path here is: compromise renderer → compromise browser process → compromise kernel via this bug. Is that right? I.e. you can't use this bug from within a renderer, you have to get into the browser process? If that is right, then I think this bug is correctly rated Medium.

If I'm wrong, and you *can* get to it directly from a renderer, then it'd be High, I think.

Thank you, lm0963hack! :)

### am...@google.com (2023-04-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-28)

Congratulations! The VRP Panel has decided to award you $5,000 for this report + $1,000 bisect bonus. Had a working poc been provided, this issue would have been potentially been eligible for a higher reward. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-04-29)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1422250?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063434)*
