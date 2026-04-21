## Title

- Use After Free in TextureVk::releaseAndDeleteImageAndViews

## Test environment

- Chromium Version

  - Chromium 100.0.4867.0 (Developer Build, 966488)
  - Chromium 100.0.4892.0 (Developer Build, 971463)

- OS : Ubuntu 20.04.3 LTS 64bit

- ** Run Option **

  - ./chrome --disable-gpu --no-sandbox http://localhost:8000/poc.html

    


## Credit
	- Jeonghoon Shin(@singi21a) at Theori

## Analysis

- https://source.chromium.org/chromium/chromium/src/+/f996d4d879434de5056e3210c8d41d28d0f15ae2:third_party/angle/src/libANGLE/renderer/vulkan/TextureVk.cpp;l=1481

  ```C++
  void TextureVk::releaseAndDeleteImageAndViews(ContextVk *contextVk)
  {
      if (mImage)
      {
          releaseStagedUpdates(contextVk); //[1]
          releaseImage(contextVk);
          mImageObserverBinding.bind(nullptr);
          mRequiresMutableStorage = false;
          mRequiredImageAccess    = vk::ImageAccess::SampleOnly;
          mImageCreateFlags       = 0;
          SafeDelete(mImage);
      }
      mBufferViews.release(contextVk);
      mRedefinedLevels.reset();
  }
  ```

  The above method is called when the texture is destroyed. In the `[1]`, call the `releaseStagedUpdates` method.

  

- https://source.chromium.org/chromium/chromium/src/+/f996d4d879434de5056e3210c8d41d28d0f15ae2:third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp;l=4737;bpv=1

```c++
void ImageHelper::releaseStagedUpdates(RendererVk *renderer)
{
    ASSERT(validateSubresourceUpdateRefCountsConsistent());

    // Remove updates that never made it to the texture.
    for (std::vector<SubresourceUpdate> &levelUpdates : mSubresourceUpdates)
    {
        for (SubresourceUpdate &update : levelUpdates)
        {
            update.release(renderer); //[2]
        }
    }

    ASSERT(validateSubresourceUpdateRefCountsConsistent());

    mSubresourceUpdates.clear();
    mCurrentSingleClearValue.reset();
}
```



In the above code,  `ImageHelper::SubresourceUpdate::release` is called `[2]`. When calling this method, Passes the already freed `renderer` object as a method argument. 

The following is the `SubresourceUpdate::release` method.

* https://source.chromium.org/chromium/chromium/src/+/f996d4d879434de5056e3210c8d41d28d0f15ae2:third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp;l=8329

  ```c++
  void ImageHelper::SubresourceUpdate::release(RendererVk *renderer)
  {
      if (updateSource == UpdateSource::Image)
      {
          refCounted.image->releaseRef();
  
          if (!refCounted.image->isReferenced())
          {
              // Staging images won't be used in render pass attachments.
              refCounted.image->get().releaseImage(renderer);
              refCounted.image->get().releaseStagedUpdates(renderer);
              SafeDelete(refCounted.image);
          }
  
          refCounted.image = nullptr;
      }
      else if (updateSource == UpdateSource::Buffer && refCounted.buffer != nullptr)
      {
          refCounted.buffer->releaseRef();
  
          if (!refCounted.buffer->isReferenced())
          {
              refCounted.buffer->get().release(renderer); //[3] UAF occur
              SafeDelete(refCounted.buffer);
          }
  
          refCounted.buffer = nullptr;
      }
  }
  ```

  In the comment `[3]`, Use After Free occurs when accessing a `renderer` object that has already been freed.

  

## PoC

- please refer to attached files.

## ASan log
- please refer to attached files.
