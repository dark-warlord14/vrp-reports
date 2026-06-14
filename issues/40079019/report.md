# Security: Integer overflow allocating shared memory in SoftwareFrameManager::SwapToNewFrame()

| Field | Value |
|-------|-------|
| **Issue ID** | [40079019](https://issues.chromium.org/issues/40079019) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>Internals, Internals>Skia, Internals>Skia>Compositing |
| **Reporter** | aa...@gmail.com |
| **Assignee** | cc...@chromium.org |
| **Created** | 2014-03-01 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

There may be an integer overflow allocating shared memory in SoftwareFrameManager::SwapToNewFrame():

```
const size_t size_in_bytes = 4 \* frame_data->size.GetArea();  

...  

if (!shared_memory->Map(size_in_bytes)) {  
  DLOG(ERROR) << "Unable to map renderer memory.";  
  RecordAction(  
      base::UserMetricsAction("BadMessageTerminate_SharedMemoryManager1"));  
  return false;  
}  

...  

scoped_refptr<SoftwareFrame> next_frame(new SoftwareFrame(  
    client_,  
    output_surface_id,  
    frame_data->id,  
    frame_device_scale_factor,  
    frame_data->size,  
    shared_memory.Pass()));  
current_frame_.swap(next_frame);  

```

In one call sequence the frame\_data passed to SoftwareFrameManager::SwapToNewFrame() is read from an ipc ViewHostMsg\_SwapCompositorFrame message:

RenderWidgetHostImpl::OnMessageReceived  

RenderWidgetHostImpl::OnSwapCompositorFrame  

RenderWidgetHostViewAura::OnSwapCompositorFrame  

RenderWidgetHostViewAura::SwapSoftwareFrame  

SoftwareFrameManager::SwapToNewFrame

If frame\_data->size.GetArea() is sufficiently large, multiplication by 4 may trigger an overflow such that the mapped memory size is less than four times the number of pixels. In this case, it appears that an attempt may then be made to draw using memory outside of the allocated shared region.

Also, there appears to be a similar potential for an overflow in TextureMailbox::shared\_memory\_size\_in\_bytes:

size\_t TextureMailbox::shared\_memory\_size\_in\_bytes() const {  

return 4 \* shared\_memory\_size\_.GetArea();  

}

PS I am new to the chromium code base and to security work in general. Apologies if I've made an error in this bug report.

**VERSION**  

Chrome Version: source git hash 785031dd5c78c21e345a2b5b8d698f42ba5ba00e with the attached patch applied to simulate a compromised renderer process.  

Operating System: Linux 3.2.0-54-virtual #82-Ubuntu SMP Tue Sep 10 20:31:18 UTC 2013 x86\_64 x86\_64 x86\_64 GNU/Linux

**REPRODUCTION CASE**  

The attached patch was applied to source git hash 785031dd5c78c21e345a2b5b8d698f42ba5ba00e (to simulate a compromised renderer process sending a cooked ViewHostMsg\_SwapCompositorFrame message). Then chrome was compiled as a 64 bit asan build. On starting chrome, it terminated with the attached asan output.

## Attachments

- [diff.patch](attachments/diff.patch) (application/octet-stream, 1.4 KB)
- [crash_symbolized.log](attachments/crash_symbolized.log) (text/plain, 10.1 KB)

## Timeline

### js...@chromium.org (2014-03-02)

The individual dimensions appear to be consistently bounded by kMaxDimension (32767) and the area appears bounded by kMaxCanvas (268,435,456). So, there shouldn't be an overflow in the locations you've identified.

That said, the fact that your patch forces the crash implies there is a legitimate bug, but it seems like it's in Skia. Either it's failing to adequately bounds check and we're triggering a different path, or maybe the GPU stack is just being too permissive about not killing the renderer on a bad message.

I'm manually adding some flags to get the right eyes on this.


### ts...@chromium.org (2014-03-03)

Actually, this is overflowing exactly as indicated:

(gdb) p frame_data->size
$24 = {
  <gfx::SizeBase<gfx::Size, int>> = {
    width_ = 1048577, 
    height_ = 1024
  }, <No data fields>}
(gdb) p size_in_bytes
$25 = 4096


### ts...@chromium.org (2014-03-03)

(Note that the --disable-gpu flag is required here to prevent the patch from segv'ing the renderer ...)

### ts...@chromium.org (2014-03-03)

I'm guessing severity high, as passing the right offsets in other places may give substantial control over the addresses used and lead to a sandbox escape.

### ts...@chromium.org (2014-03-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-12)

ccameron@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cc...@chromium.org (2014-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-03-17)

------------------------------------------------------------------
r257417 | ccameron@chromium.org | 2014-03-17T13:40:33.897829Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/renderer_host/software_frame_manager.cc?r1=257417&r2=257416&pathrev=257417

Fix integer overflow in software compositor

Ensure that the size mapped from the renderer
process for the software frame is not less than
expected due to integer overflow.

BUG=348332

Review URL: https://codereview.chromium.org/196283018
-----------------------------------------------------------------

### in...@chromium.org (2014-03-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-17)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### js...@chromium.org (2014-03-19)

[Empty comment from Monorail migration]

### da...@chromium.org (2014-03-19)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-03-20)

------------------------------------------------------------------
r258418 | danakj@chromium.org | 2014-03-20T21:43:39.660560Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/common/cc_messages_unittest.cc?r1=258418&r2=258417&pathrev=258418
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/renderer_host/software_frame_manager.cc?r1=258418&r2=258417&pathrev=258418
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/common/cc_messages.cc?r1=258418&r2=258417&pathrev=258418
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/common/cc_messages.h?r1=258418&r2=258417&pathrev=258418
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/output/software_frame_data.cc?r1=258418&r2=258417&pathrev=258418
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/output/software_frame_data.h?r1=258418&r2=258417&pathrev=258418

Move SoftwareFrameData overflow checks to the IPC code.

Instead of doing this check in SoftwareFrameManager and silently
dropping the frame, if we have an overflow, drop the IPC from the
renderer (and cause a renderer crash which we can see).

Also move computation code for the frame size in bytes to
SoftwareFrameData so the computation and the check can be beside
each other.

Also add unit tests for SoftwareFrameData IPC.

R=ccameron@chromium.org, jschuh@chromium.org, piman@chromium.org, ccameron, piman
BUG=348332

Review URL: https://codereview.chromium.org/196423027
-----------------------------------------------------------------

### da...@chromium.org (2014-03-20)

So, we want to merge 258418 to 34? Was the previous one merged at all? It appears not?

### cc...@chromium.org (2014-03-20)

It hasn't been merged. Both sounds good -- want me to do them both?

### da...@chromium.org (2014-03-20)

Sure sure, let's see what the TPMs say though.

### dx...@chromium.org (2014-03-21)

how does this look on canary?

### dx...@chromium.org (2014-03-21)

approved for M34/1847.

### bu...@chromium.org (2014-03-23)

------------------------------------------------------------------
r258722 | ccameron@chromium.org | 2014-03-22T00:37:36.241190Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/content/browser/renderer_host/software_frame_manager.cc?r1=258722&r2=258721&pathrev=258722

Merge 257417 "Fix integer overflow in software compositor"

> Fix integer overflow in software compositor
> 
> Ensure that the size mapped from the renderer
> process for the software frame is not less than
> expected due to integer overflow.
> 
> BUG=348332
> 
> Review URL: https://codereview.chromium.org/196283018

TBR=ccameron@chromium.org

Review URL: https://codereview.chromium.org/204733006
-----------------------------------------------------------------

### bu...@chromium.org (2014-03-23)

------------------------------------------------------------------
r258737 | ccameron@chromium.org | 2014-03-22T01:37:18.209556Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/content/browser/renderer_host/software_frame_manager.cc?r1=258737&r2=258736&pathrev=258737

Revert 258722 "Merge 257417 "Fix integer overflow in software co..."

> Merge 257417 "Fix integer overflow in software compositor"
> 
> > Fix integer overflow in software compositor
> > 
> > Ensure that the size mapped from the renderer
> > process for the software frame is not less than
> > expected due to integer overflow.
> > 
> > BUG=348332
> > 
> > Review URL: https://codereview.chromium.org/196283018
> 
> TBR=ccameron@chromium.org
> 
> Review URL: https://codereview.chromium.org/204733006

TBR=ccameron@chromium.org

Review URL: https://codereview.chromium.org/207503003
-----------------------------------------------------------------

### ti...@chromium.org (2014-03-28)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-03-28)

[Empty comment from Monorail migration]

### aa...@gmail.com (2014-03-31)

Hi folks,

I wanted to follow up on the potential overflow in TextureMailbox::shared_memory_size_in_bytes(), which I mentioned in passing in the initial bug report:

size_t TextureMailbox::shared_memory_size_in_bytes() const {
  return 4 * shared_memory_size_.GetArea();
}

Please consider the following excerpt from RenderWidgetHostViewAura::OnLayerRecreated():

    base::SharedMemory* old_buffer = old_mailbox.shared_memory();
    const size_t size = old_mailbox.shared_memory_size_in_bytes();

    scoped_ptr<base::SharedMemory> new_buffer(new base::SharedMemory);
    new_buffer->CreateAndMapAnonymous(size);

    if (old_buffer->memory() && new_buffer->memory()) {
      memcpy(new_buffer->memory(), old_buffer->memory(), size);
      base::SharedMemory* new_buffer_raw_ptr = new_buffer.get();
      scoped_ptr<cc::SingleReleaseCallback> callback =
          cc::SingleReleaseCallback::Create(base::Bind(MailboxReleaseCallback,
                                                       Passed(&new_buffer)));
      cc::TextureMailbox new_mailbox(new_buffer_raw_ptr,
                                     old_mailbox.shared_memory_size());
      new_layer->SetTextureMailbox(new_mailbox,
                                   callback.Pass(),
                                   mailbox_scale_factor);
    }


It seems that even if the overflow is avoided in SoftwareFrameManager::SwapToNewFrame(), given a sufficiently large frame size the value computed in TextureMailbox::shared_memory_size_in_bytes() may overflow causing the ‘size’ used by RenderWidgetHostViewAura::OnLayerRecreated() to be less than 4 times the number of pixels in the old layer.  In turn, ‘new_mailbox’ may refer to a shared memory region smaller than 4 times its shared_memory_size().GetArea().

### pi...@chromium.org (2014-03-31)

If it overflows in SwapToNewFrame, we reject the frame, so it won't be passed later to OnLayerRecreated. Is there a case where it would not overflow in SwapToNewFrame but would later on in shared_memory_size_in_bytes() ? AFAICT both use the same information (width*height*4).

### da...@chromium.org (2014-03-31)

GetArea() does (signed) integer multiplication, where as the SoftwareFrameData does size_t multiplication.

I'm looking at some solutions now.

### da...@chromium.org (2014-03-31)

IMO I think the current GetArea() should just be considered Harmful.

### aa...@gmail.com (2014-03-31)

@danakj - Yes, the fact that the new overflow checking in ParamTraits<cc::SoftwareFrameData>::Read() converts to size_t before multiplication while the older calculation in shared_memory_size_in_bytes() just multiplies ints means they have different overflow conditions, and this is what I had in mind.  Sorry, I probably should have written that explicitly.

### da...@chromium.org (2014-03-31)

This code is dead as of recently since we have ubercomp on for software compositing though, anyhow, I guess.

### aa...@gmail.com (2014-03-31)

Ok thanks, good to know.  I noticed one additional allocation based on shared_memory_size_in_bytes() in TextureLayerImpl::WillDraw() - not sure if that is in live or dead code.   I am probably not going to try and write test / trigger cases for these (unless it affects the reward process), but I thought I would report / ask about them in case helpful.

### da...@chromium.org (2014-03-31)

Ya, it's the same function, I'll look at it.

### bu...@chromium.org (2014-04-01)

------------------------------------------------------------------
r260969 | danakj@chromium.org | 2014-04-01T22:59:15.526432Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/resources/texture_mailbox.cc?r1=260969&r2=260968&pathrev=260969
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/resources/texture_mailbox.h?r1=260969&r2=260968&pathrev=260969
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/layers/texture_layer_impl.cc?r1=260969&r2=260968&pathrev=260969
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/renderer_host/render_widget_host_view_aura.cc?r1=260969&r2=260968&pathrev=260969

cc: Prevent integer overflow with software TextureMailbox.

Perform a CHECK() when creating a software TextureMailbox since these
come from outside of cc's control.

Do unsigned integer multiplication to produce an unsigned result,
preventing overflow when possible.

R=piman@chromium.org
BUG=348332

Review URL: https://codereview.chromium.org/220093002
-----------------------------------------------------------------

### bu...@chromium.org (2014-04-04)

------------------------------------------------------------------
r261817 | danakj@chromium.org | 2014-04-04T19:01:21.464949Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/renderer_host/software_frame_manager.cc?r1=261817&r2=261816&pathrev=261817
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/common/cc_messages.cc?r1=261817&r2=261816&pathrev=261817
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/resources/resource_provider.cc?r1=261817&r2=261816&pathrev=261817
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/layers/texture_layer_impl.cc?r1=261817&r2=261816&pathrev=261817
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/resources/shared_bitmap.cc?r1=261817&r2=261816&pathrev=261817
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/output/software_frame_data.cc?r1=261817&r2=261816&pathrev=261817
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/resources/shared_bitmap.h?r1=261817&r2=261816&pathrev=261817
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/output/software_frame_data.h?r1=261817&r2=261816&pathrev=261817
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/resources/texture_mailbox.cc?r1=261817&r2=261816&pathrev=261817
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/common/host_shared_bitmap_manager_unittest.cc?r1=261817&r2=261816&pathrev=261817
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/common/host_shared_bitmap_manager.cc?r1=261817&r2=261816&pathrev=261817
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/resources/texture_mailbox.h?r1=261817&r2=261816&pathrev=261817
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/child/child_shared_bitmap_manager.cc?r1=261817&r2=261816&pathrev=261817

cc: Remove all usage of GetArea() from production code in cc

Consolidate the calls to turn gfx::Size into a number of bytes onto
the cc::SharedBitmap class. The class offers the following methods:
1. Get a size_t bytes and bool saying if you overflowed or not.
2. Get a size_t bytes and crash if you overflow.
3. Get a size_t bytes and don't check for overflow.
4. Tell me if the gfx::Size would overflow to create the size_t bytes.

These were the use cases I found in the existing code, plus the
addition of case 2. A few places that were finding the size_t bytes
without looking for overflow (case 3), from a previously-unchecked
gfx::Size, were changed to crash on overflow instead (case 2).

R=jbauman@chromium.org, piman@chromium.org
BUG=348332

Review URL: https://codereview.chromium.org/221523003
-----------------------------------------------------------------

### [Deleted User] (2014-04-04)

@aaron.staple: I wanted to offer you a note of encouragement. When you say "PS I am new to the chromium code base and to security work in general.  Apologies if I've made an error in this bug report" -- it's a great bug and the report is of excellent quality!

### aa...@gmail.com (2014-04-04)

@cevans - Thank you!

### in...@chromium.org (2014-04-05)

Aaron, how would you like to credited in the release notes.

### ti...@chromium.org (2014-04-05)

[Comment Deleted]

### ti...@chromium.org (2014-04-05)

[Comment Deleted]

### ti...@chromium.org (2014-04-05)

[Empty comment from Monorail migration]

### aa...@gmail.com (2014-04-05)

You can just use my name: Aaron Staple
Thanks!

### bu...@chromium.org (2014-04-05)

------------------------------------------------------------------
r261972 | scottmg@chromium.org | 2014-04-05T07:20:06.649985Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/resources/texture_mailbox.cc?r1=261972&r2=261971&pathrev=261972
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/common/host_shared_bitmap_manager_unittest.cc?r1=261972&r2=261971&pathrev=261972
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/common/host_shared_bitmap_manager.cc?r1=261972&r2=261971&pathrev=261972
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/resources/texture_mailbox.h?r1=261972&r2=261971&pathrev=261972
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/child/child_shared_bitmap_manager.cc?r1=261972&r2=261971&pathrev=261972
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/renderer_host/software_frame_manager.cc?r1=261972&r2=261971&pathrev=261972
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/common/cc_messages.cc?r1=261972&r2=261971&pathrev=261972
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/resources/resource_provider.cc?r1=261972&r2=261971&pathrev=261972
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/layers/texture_layer_impl.cc?r1=261972&r2=261971&pathrev=261972
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/resources/shared_bitmap.cc?r1=261972&r2=261971&pathrev=261972
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/output/software_frame_data.cc?r1=261972&r2=261971&pathrev=261972
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/resources/shared_bitmap.h?r1=261972&r2=261971&pathrev=261972
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/output/software_frame_data.h?r1=261972&r2=261971&pathrev=261972

Revert 261817 "cc: Remove all usage of GetArea() from production..."

Suspected of causing failures on Linux CrOS ASan LSan:

http://build.chromium.org/p/chromium.memory/builders/Linux%20Chromium%20OS%20ASan%2BLSan%20Tests%20%283%29/builds/702

http://build.chromium.org/p/chromium.memory/builders/Linux%20Chromium%20OS%20ASan%2BLSan%20Tests%20%282%29/builds/664

http://build.chromium.org/p/chromium.memory/builders/Linux%20Chromium%20OS%20ASan%2BLSan%20Tests%20%281%29/builds/702


> cc: Remove all usage of GetArea() from production code in cc
> 
> Consolidate the calls to turn gfx::Size into a number of bytes onto
> the cc::SharedBitmap class. The class offers the following methods:
> 1. Get a size_t bytes and bool saying if you overflowed or not.
> 2. Get a size_t bytes and crash if you overflow.
> 3. Get a size_t bytes and don't check for overflow.
> 4. Tell me if the gfx::Size would overflow to create the size_t bytes.
> 
> These were the use cases I found in the existing code, plus the
> addition of case 2. A few places that were finding the size_t bytes
> without looking for overflow (case 3), from a previously-unchecked
> gfx::Size, were changed to crash on overflow instead (case 2).
> 
> R=jbauman@chromium.org, piman@chromium.org
> BUG=348332
> 
> Review URL: https://codereview.chromium.org/221523003

TBR=danakj@chromium.org

Review URL: https://codereview.chromium.org/226693005
-----------------------------------------------------------------

### bu...@chromium.org (2014-04-05)

------------------------------------------------------------------
r262022 | scottmg@chromium.org | 2014-04-05T17:58:16.992298Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/output/software_frame_data.h?r1=262022&r2=262021&pathrev=262022
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/resources/texture_mailbox.cc?r1=262022&r2=262021&pathrev=262022
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/common/host_shared_bitmap_manager_unittest.cc?r1=262022&r2=262021&pathrev=262022
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/common/host_shared_bitmap_manager.cc?r1=262022&r2=262021&pathrev=262022
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/resources/texture_mailbox.h?r1=262022&r2=262021&pathrev=262022
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/child/child_shared_bitmap_manager.cc?r1=262022&r2=262021&pathrev=262022
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/renderer_host/software_frame_manager.cc?r1=262022&r2=262021&pathrev=262022
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/common/cc_messages.cc?r1=262022&r2=262021&pathrev=262022
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/resources/resource_provider.cc?r1=262022&r2=262021&pathrev=262022
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/layers/texture_layer_impl.cc?r1=262022&r2=262021&pathrev=262022
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/resources/shared_bitmap.cc?r1=262022&r2=262021&pathrev=262022
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/output/software_frame_data.cc?r1=262022&r2=262021&pathrev=262022
   M http://src.chromium.org/viewvc/chrome/trunk/src/cc/resources/shared_bitmap.h?r1=262022&r2=262021&pathrev=262022

Revert 261972 "Revert 261817 "cc: Remove all usage of GetArea() ..."

r261817 falsely accused! Reverting the revert, sorry for the noise.

> Revert 261817 "cc: Remove all usage of GetArea() from production..."
> 
> Suspected of causing failures on Linux CrOS ASan LSan:
> 
> http://build.chromium.org/p/chromium.memory/builders/Linux%20Chromium%20OS%20ASan%2BLSan%20Tests%20%283%29/builds/702
> 
> http://build.chromium.org/p/chromium.memory/builders/Linux%20Chromium%20OS%20ASan%2BLSan%20Tests%20%282%29/builds/664
> 
> http://build.chromium.org/p/chromium.memory/builders/Linux%20Chromium%20OS%20ASan%2BLSan%20Tests%20%281%29/builds/702
> 
> 
> > cc: Remove all usage of GetArea() from production code in cc
> > 
> > Consolidate the calls to turn gfx::Size into a number of bytes onto
> > the cc::SharedBitmap class. The class offers the following methods:
> > 1. Get a size_t bytes and bool saying if you overflowed or not.
> > 2. Get a size_t bytes and crash if you overflow.
> > 3. Get a size_t bytes and don't check for overflow.
> > 4. Tell me if the gfx::Size would overflow to create the size_t bytes.
> > 
> > These were the use cases I found in the existing code, plus the
> > addition of case 2. A few places that were finding the size_t bytes
> > without looking for overflow (case 3), from a previously-unchecked
> > gfx::Size, were changed to crash on overflow instead (case 2).
> > 
> > R=jbauman@chromium.org, piman@chromium.org
> > BUG=348332
> > 
> > Review URL: https://codereview.chromium.org/221523003
> 
> TBR=danakj@chromium.org
> 
> Review URL: https://codereview.chromium.org/226693005

TBR=scottmg@chromium.org, danakj@chromium.org

Review URL: https://codereview.chromium.org/226693007
-----------------------------------------------------------------

### ti...@chromium.org (2014-04-14)

Thanks for the report - $3000 for this one. I'll start the payment process today.

### ti...@chromium.org (2014-04-15)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-28)

Processing via our e-payment system can take up to 30 days, but the reward should be on its way to you. Please do NOT publicly disclose details until a fix has been released to all our users. Thanks again for your help!

### cl...@chromium.org (2014-06-23)

Bulk update: removing view restriction from closed bugs.

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/348332?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>GPU>Internals, Internals>Skia, Internals>Skia>Compositing]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079019)*
