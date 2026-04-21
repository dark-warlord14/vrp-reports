# Security: TALOS-2023-1724 - Google Chrome WebGL rx::Image11::disassociateStorage use-after-free vulnerability 

| Field | Value |
|-------|-------|
| **Issue ID** | [40063051](https://issues.chromium.org/issues/40063051) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL, Internals>GPU>ANGLE |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | pi...@thelead82.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2023-02-13 |
| **Bounty** | $15,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

A use-after-free vulnerability exists in the WebGL rx::Image11::disassociateStorage functionality of Google Chrome Stable 110.0.5481.78 (64-bit) / Chromium 112.0.5592.0 (Build) (64-bit). A specially-crafted web page can lead to a use-after-free. An attacker can create special website to trigger this vulnerability.

**VERSION**  

Google Chrome Stable 110.0.5481.78 (64-bit)  

Chromium 112.0.5592.0 (Build) (64-bit)

**REPRODUCTION CASE**  

Attached

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

POC command line: chrome.exe --no-sandbox --disable-gpu-sandbox C:\poc\poc.html

```
=================================================================  
==10188==ERROR: AddressSanitizer: heap-use-after-free on address 0x120fcd16f880 at pc 0x7fffe9981346 bp 0x0058403fdb60 sp 0x0058403fdba8  
READ of size 8 at 0x120fcd16f880 thread T0  
==10188==WARNING: Failed to use and restart external symbolizer!  
==10188==\*\*\* WARNING: Failed to initialize DbgHelp!              \*\*\*  
==10188==\*\*\* Most likely this means that the app is already      \*\*\*  
==10188==\*\*\* using DbgHelp, possibly with incompatible flags.    \*\*\*  
==10188==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  
==10188==\*\*\* or produce wrong results.                           \*\*\*  
    #0 0x7fffe9981345 in rx::Image11::disassociateStorage C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Image11.cpp:216  
    #1 0x7fffe9983d95 in rx::Image11::redefine C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Image11.cpp:234  
    #2 0x7fffe9ac676b in rx::TextureD3D_2D::redefineImage C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp:1710  
    #3 0x7fffe9acb670 in rx::TextureD3D_2D::setEGLImageTarget C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp:1439  
    #4 0x7fffe97e78cf in gl::Texture::setEGLImageTargetImpl C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Texture.cpp:1905  
    #5 0x7fffe97e7a79 in gl::Texture::setEGLImageTarget C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Texture.cpp:1919  
    #6 0x7fffe92dad94 in GL_EGLImageTargetTexture2DOES C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libGLESv2\entry_points_gles_ext_autogen.cpp:10013  
    #7 0x7fff8af4755e in gl::GLImageD3D::BindTexImage C:\b\s\w\ir\cache\builder\src\ui\gl\gl_image_d3d.cc:80  
    #8 0x7fff86eeb0f5 in gpu::D3DImageBacking::PresentSwapChain C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\shared_image\d3d_image_backing.cc:993  
    #9 0x7fff86ef8214 in gpu::SharedImageFactory::PresentSwapChain C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\shared_image\shared_image_factory.cc:558  
    #10 0x7fff8478a993 in gpu::SharedImageStub::OnPresentSwapChain C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\shared_image_stub.cc:427  
    #11 0x7fff84786d6c in gpu::SharedImageStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\shared_image_stub.cc:118  
    #12 0x7fff80e0e3ef in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:709  
    #13 0x7fff80e1cde0 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:970  
    #14 0x7fff808299f6 in gpu::SchedulerDfs::ExecuteSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:763  
    #15 0x7fff80827af4 in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:674  
    #16 0x7fff8083038f in base::internal::Invoker<base::internal::BindState<void (gpu::SchedulerDfs::\*)(),base::internal::UnretainedWrapper<gpu::SchedulerDfs,base::unretained_traits::MayNotDangle> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:970  
    #17 0x7fff7c1a3567 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:165  
    #18 0x7fff7f554257 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:489  
    #19 0x7fff7f552d73 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:340  
    #20 0x7fff7f523833 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:48  
    #21 0x7fff7f556bc7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:649  
    #22 0x7fff7c127141 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:140  
    #23 0x7fff7ec5b2c1 in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc:399  
    #24 0x7fff7a9abd93 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:760  
    #25 0x7fff7a9aeaf4 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1122  
    #26 0x7fff7a9a95c4 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:335  
    #27 0x7fff7a9aa4b4 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:363  
    #28 0x7fff6ee71699 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:190  
    #29 0x7ff7b2506378 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:166  
    #30 0x7ff7b2502bb1 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:391  
    #31 0x7ff7b296d62b in __scrt_common_main_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288  
    #32 0x7ff843da7613 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017613)  
    #33 0x7ff8442c26a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)  

```

[..]

**CREDIT INFORMATION**

Reporter credit: Piotr Bania of Cisco Talos

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 2.3 KB)
- [TALOS-2023-1724 - Google_Chrome_WebGL_rx Image11 disassociateStorage_use-after-free_vulnerability.txt](attachments/TALOS-2023-1724 - Google_Chrome_WebGL_rx Image11 disassociateStorage_use-after-free_vulnerability.txt) (text/plain, 28.0 KB)

## Timeline

### vu...@sourcefire.com (2023-02-13)

Details

Google Chrome is a cross-platform web browser developed by Google and is currently the most popular web browser. It supports many features including WebGL (Web Graphics Library), which is a JavaScript API for rendering 2D and 3D graphics.

This vulnerability happens in ANGLE library (compatibility layer between OpenGL and Direct3D) used by Google Chrome browser.

Problem happens in the redefineImage function:

    // libANGLE/renderer/d3d/TextureD3D.cpp


    angle::Result TextureD3D_2D::redefineImage(const gl::Context *context,
                                               size_t level,
                                               GLenum internalformat,
                                               const gl::Extents &size,
                                               bool forceRelease)
    {
        ASSERT(size.depth == 1);
        // If there currently is a corresponding storage texture image, it has these parameters
        const int storageWidth     = std::max(1, getLevelZeroWidth() >> level);
        const int storageHeight    = std::max(1, getLevelZeroHeight() >> level);
        const GLenum storageFormat = getBaseLevelInternalFormat();
        if (mTexStorage)
        {
            const size_t storageLevels = mTexStorage->getLevelCount();
            // If the storage was from an EGL image, copy it back into local images to preserve it
            // while orphaning
            if (level != 0 && mEGLImageTarget)
            {
                ANGLE_TRY(mImageArray[0]->copyFromTexStorage(context, gl::ImageIndex::Make2D(0),
                                                             mTexStorage));
            }
            if ((level >= storageLevels && storageLevels != 0) || size.width != storageWidth ||
                size.height != storageHeight || internalformat != storageFormat ||
                mEGLImageTarget)  // Discard mismatched storage
            {
                gl::TexLevelMask copyImageMask;
                copyImageMask.set();
                copyImageMask.set(level, false);
                ANGLE_TRY(releaseTexStorage(context, copyImageMask));
                markAllImagesDirty();
            }
        }
        mImageArray[level]->redefine(gl::TextureType::_2D, internalformat, size, forceRelease);
        mDirtyImages = mDirtyImages || mImageArray[level]->isDirty();
        // Can't be an EGL image target after being redefined
        mEGLImageTarget = false;
        return angle::Result::Continue;
    }

In the code above, firstly the releaseTexStorage function will be executed (because of the mEGLImageTarget argument). Secondly the redefine function is executed.
The redefine function will call the disassociateStorage function, however at this point the mAssociatedStorage object is already freed (by the releaseTexStorage).

Use after free happens in Image11::disassociateStorage() function (in src/libANGLE/renderer/d3d/d3d11/Image11.cpp), because the mRecoverFromStorage variable and the mAssociatedStorage object being already freed.

    bool Image11::redefine(gl::TextureType type,
                           GLenum internalformat,
                           const gl::Extents &size,
                           bool forceRelease)
    {
        if (mWidth != size.width || mHeight != size.height || mDepth != size.depth ||
            mInternalFormat != internalformat || forceRelease)
        {
            // End the association with the TextureStorage, since that data will be out of date.
            // Also reset mRecoveredFromStorageCount since this Image is getting completely redefined.
            disassociateStorage(); // magic call
            ...






    // user after free happens in this function
    void Image11::disassociateStorage()
    {
        if (mRecoverFromStorage)
        {
            // Make the texturestorage release the Image11 too
            mAssociatedStorage->disassociateImage(mAssociatedImageIndex, this); // use after free

            mRecoverFromStorage   = false;
            mAssociatedStorage    = nullptr;
            mAssociatedImageIndex = gl::ImageIndex();
        }
    }

Like we have previously mentioned in order for the use-after-free to happen mRecoverFromStorage needs to be set. This is done in copyToStorage function:

    angle::Result Image11::copyToStorage(const gl::Context *context,
                                         TextureStorage *storage,
                                         const gl::ImageIndex &index,
                                         const gl::Box &region)
    {
        TextureStorage11 *storage11 = GetAs<TextureStorage11>(storage);
        // If an app's behavior results in an Image11 copying its data to/from to a TextureStorage
        // multiple times, then we should just keep the staging texture around to prevent the copying
        // from impacting perf. We allow the Image11 to copy its data to/from TextureStorage once. This
        // accounts for an app making a late call to glGenerateMipmap.
        bool attemptToReleaseStagingTexture = (mRecoveredFromStorageCount < 2);
        if (attemptToReleaseStagingTexture)
        {
            // If another image is relying on this Storage for its data, then we must let it recover its
            // data before we overwrite it.
            ANGLE_TRY(storage11->releaseAssociatedImage(context, index, this));
        }
        const TextureHelper11 *stagingTexture = nullptr;
        unsigned int stagingSubresourceIndex  = 0;
        ANGLE_TRY(getStagingTexture(context, &stagingTexture, &stagingSubresourceIndex));
        ANGLE_TRY(storage11->updateSubresourceLevel(context, *stagingTexture, stagingSubresourceIndex,
                                                    index, region));
        // Once the image data has been copied into the Storage, we can release it locally.
        if (attemptToReleaseStagingTexture)
        {
            storage11->associateImage(this, index);
            releaseStagingTexture();
            mRecoverFromStorage   = true;           // set mRecoverFromStorage
            mAssociatedStorage    = storage11;
            mAssociatedImageIndex = index;
        }
        return angle::Result::Continue;
    }

In order to execute the copyToStorage function (and set the mRecoverFromStorage var) we need to force chrome to i.e. execute TextureD3D_2D::copySubTexture, pass the initial checks and use commitRegion function, commitRegion will finally call the copyToStorage:

    // src/libANGLE/renderer/d3d/TextureD3D.cpp
    angle::Result TextureD3D_2D::copySubTexture(const gl::Context *context,
                                                const gl::ImageIndex &index,
                                                const gl::Offset &destOffset,
                                                GLint sourceLevel,
                                                const gl::Box &sourceBox,
                                                bool unpackFlipY,
                                                bool unpackPremultiplyAlpha,
                                                bool unpackUnmultiplyAlpha,
                                                const gl::Texture *source)
    {
        ASSERT(index.getTarget() == gl::TextureTarget::_2D);
        if (!isSRGB(index.getLevelIndex()) && canCreateRenderTargetForImage(index))
        {
            // WE ARE NOT INTERESTED IN THIS

            ANGLE_TRY(ensureRenderTarget(context));
            ASSERT(isValidLevel(index.getLevelIndex()));
            ANGLE_TRY(updateStorageLevel(context, index.getLevelIndex()));
            const gl::InternalFormat &internalFormatInfo =
                gl::GetSizedInternalFormatInfo(getInternalFormat(index.getLevelIndex()));
            ANGLE_TRY(mRenderer->copyTexture(context, source, sourceLevel, gl::TextureTarget::_2D,
                                             sourceBox, internalFormatInfo.format,
                                             internalFormatInfo.type, destOffset, mTexStorage,
                                             index.getTarget(), index.getLevelIndex(), unpackFlipY,
                                             unpackPremultiplyAlpha, unpackUnmultiplyAlpha));
        }
        else
        {
            gl::ImageIndex sourceImageIndex = gl::ImageIndex::Make2D(sourceLevel);
            TextureD3D *sourceD3D           = GetImplAs<TextureD3D>(source);
            ImageD3D *sourceImage           = nullptr;
            ANGLE_TRY(sourceD3D->getImageAndSyncFromStorage(context, sourceImageIndex, &sourceImage));
            ImageD3D *destImage = nullptr;
            ANGLE_TRY(getImageAndSyncFromStorage(context, index, &destImage));
            ANGLE_TRY(mRenderer->copyImage(context, destImage, sourceImage, sourceBox, destOffset,
                                           unpackFlipY, unpackPremultiplyAlpha, unpackUnmultiplyAlpha));
            mDirtyImages = true;
            gl::Box destRegion(destOffset.x, destOffset.y, 0, sourceBox.width, sourceBox.height, 1);
            ANGLE_TRY(commitRegion(context, index, destRegion));
        }
        return angle::Result::Continue;
    }

To pass the first check we need to force the canCreateRenderTargetForImage(index) condition to be false. We can do this by using the gl.texParameteri and gl.texImage2D function as shown in the poc code. commitRegion will lead to the execution of copyToStorage, which will set the mRecoverFromStorage. Leading later to use-after-free as mentioned above.

Final note: the webgl2 context needs to be created with desynchronized option set to true (boolean that hints the user agent to reduce the latency by desynchronizing the canvas paint cycle from the event loop) in order for this vulnerability to happen.
Crash Information

    POC command line: chrome.exe --no-sandbox --disable-gpu-sandbox C:\poc\poc.html




    =================================================================
    ==10188==ERROR: AddressSanitizer: heap-use-after-free on address 0x120fcd16f880 at pc 0x7fffe9981346 bp 0x0058403fdb60 sp 0x0058403fdba8
    READ of size 8 at 0x120fcd16f880 thread T0
    ==10188==WARNING: Failed to use and restart external symbolizer!
    ==10188==*** WARNING: Failed to initialize DbgHelp!              ***
    ==10188==*** Most likely this means that the app is already      ***
    ==10188==*** using DbgHelp, possibly with incompatible flags.    ***
    ==10188==*** Due to technical reasons, symbolization might crash ***
    ==10188==*** or produce wrong results.                           ***
        #0 0x7fffe9981345 in rx::Image11::disassociateStorage C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Image11.cpp:216
        #1 0x7fffe9983d95 in rx::Image11::redefine C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Image11.cpp:234
        #2 0x7fffe9ac676b in rx::TextureD3D_2D::redefineImage C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp:1710
        #3 0x7fffe9acb670 in rx::TextureD3D_2D::setEGLImageTarget C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp:1439
        #4 0x7fffe97e78cf in gl::Texture::setEGLImageTargetImpl C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Texture.cpp:1905
        #5 0x7fffe97e7a79 in gl::Texture::setEGLImageTarget C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Texture.cpp:1919
        #6 0x7fffe92dad94 in GL_EGLImageTargetTexture2DOES C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libGLESv2\entry_points_gles_ext_autogen.cpp:10013
        #7 0x7fff8af4755e in gl::GLImageD3D::BindTexImage C:\b\s\w\ir\cache\builder\src\ui\gl\gl_image_d3d.cc:80
        #8 0x7fff86eeb0f5 in gpu::D3DImageBacking::PresentSwapChain C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\shared_image\d3d_image_backing.cc:993
        #9 0x7fff86ef8214 in gpu::SharedImageFactory::PresentSwapChain C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\shared_image\shared_image_factory.cc:558
        #10 0x7fff8478a993 in gpu::SharedImageStub::OnPresentSwapChain C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\shared_image_stub.cc:427
        #11 0x7fff84786d6c in gpu::SharedImageStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\shared_image_stub.cc:118
        #12 0x7fff80e0e3ef in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:709
        #13 0x7fff80e1cde0 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:970
        #14 0x7fff808299f6 in gpu::SchedulerDfs::ExecuteSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:763
        #15 0x7fff80827af4 in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:674
        #16 0x7fff8083038f in base::internal::Invoker<base::internal::BindState<void (gpu::SchedulerDfs::*)(),base::internal::UnretainedWrapper<gpu::SchedulerDfs,base::unretained_traits::MayNotDangle> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:970
        #17 0x7fff7c1a3567 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:165
        #18 0x7fff7f554257 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:489
        #19 0x7fff7f552d73 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:340
        #20 0x7fff7f523833 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:48
        #21 0x7fff7f556bc7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:649
        #22 0x7fff7c127141 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:140
        #23 0x7fff7ec5b2c1 in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc:399
        #24 0x7fff7a9abd93 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:760
        #25 0x7fff7a9aeaf4 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1122
        #26 0x7fff7a9a95c4 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:335
        #27 0x7fff7a9aa4b4 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:363
        #28 0x7fff6ee71699 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:190
        #29 0x7ff7b2506378 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:166
        #30 0x7ff7b2502bb1 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:391
        #31 0x7ff7b296d62b in __scrt_common_main_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
        #32 0x7ff843da7613 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017613)
        #33 0x7ff8442c26a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

    0x120fcd16f880 is located 0 bytes inside of 2600-byte region [0x120fcd16f880,0x120fcd1702a8)
    freed by thread T0 here:
        #0 0x7ff7b25b1d8d in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
        #1 0x7fffe9a303ef in rx::TextureStorage11_EGLImage::~TextureStorage11_EGLImage C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\TextureStorage11.cpp:1899
        #2 0x7fffe9ac3f5b in rx::TextureD3D::releaseTexStorage C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp:783
        #3 0x7fffe9ac6698 in rx::TextureD3D_2D::redefineImage C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp:1705
        #4 0x7fffe9acb670 in rx::TextureD3D_2D::setEGLImageTarget C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp:1439
        #5 0x7fffe97e78cf in gl::Texture::setEGLImageTargetImpl C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Texture.cpp:1905
        #6 0x7fffe97e7a79 in gl::Texture::setEGLImageTarget C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Texture.cpp:1919
        #7 0x7fffe92dad94 in GL_EGLImageTargetTexture2DOES C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libGLESv2\entry_points_gles_ext_autogen.cpp:10013
        #8 0x7fff8af4755e in gl::GLImageD3D::BindTexImage C:\b\s\w\ir\cache\builder\src\ui\gl\gl_image_d3d.cc:80
        #9 0x7fff86eeb0f5 in gpu::D3DImageBacking::PresentSwapChain C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\shared_image\d3d_image_backing.cc:993
        #10 0x7fff86ef8214 in gpu::SharedImageFactory::PresentSwapChain C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\shared_image\shared_image_factory.cc:558
        #11 0x7fff8478a993 in gpu::SharedImageStub::OnPresentSwapChain C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\shared_image_stub.cc:427
        #12 0x7fff84786d6c in gpu::SharedImageStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\shared_image_stub.cc:118
        #13 0x7fff80e0e3ef in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:709
        #14 0x7fff80e1cde0 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:970
        #15 0x7fff808299f6 in gpu::SchedulerDfs::ExecuteSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:763
        #16 0x7fff80827af4 in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:674
        #17 0x7fff8083038f in base::internal::Invoker<base::internal::BindState<void (gpu::SchedulerDfs::*)(),base::internal::UnretainedWrapper<gpu::SchedulerDfs,base::unretained_traits::MayNotDangle> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:970
        #18 0x7fff7c1a3567 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:165
        #19 0x7fff7f554257 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:489
        #20 0x7fff7f552d73 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:340
        #21 0x7fff7f523833 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:48
        #22 0x7fff7f556bc7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:649
        #23 0x7fff7c127141 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:140
        #24 0x7fff7ec5b2c1 in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc:399
        #25 0x7fff7a9abd93 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:760
        #26 0x7fff7a9aeaf4 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1122
        #27 0x7fff7a9a95c4 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:335

    previously allocated by thread T0 here:
        #0 0x7ff7b25b1e8d in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
        #1 0x7fffea10e42a in operator new d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
        #2 0x7fffe99c3348 in rx::Renderer11::createTextureStorageEGLImage C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Renderer11.cpp:3396
        #3 0x7fffe9acb900 in rx::TextureD3D_2D::setEGLImageTarget C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp:1455
        #4 0x7fffe97e78cf in gl::Texture::setEGLImageTargetImpl C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Texture.cpp:1905
        #5 0x7fffe97e7a79 in gl::Texture::setEGLImageTarget C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Texture.cpp:1919
        #6 0x7fffe92dad94 in GL_EGLImageTargetTexture2DOES C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libGLESv2\entry_points_gles_ext_autogen.cpp:10013
        #7 0x7fff8af4755e in gl::GLImageD3D::BindTexImage C:\b\s\w\ir\cache\builder\src\ui\gl\gl_image_d3d.cc:80
        #8 0x7fff86ede2db in gpu::D3DImageBacking::CreateGLTexture C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\shared_image\d3d_image_backing.cc:189
        #9 0x7fff86edf66e in gpu::D3DImageBacking::CreateFromSwapChainBuffer C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\shared_image\d3d_image_backing.cc:230
        #10 0x7fff82329602 in gpu::D3DImageBackingFactory::CreateSwapChain C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\shared_image\d3d_image_backing_factory.cc:314
        #11 0x7fff86ef7ef3 in gpu::SharedImageFactory::CreateSwapChain C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\shared_image\shared_image_factory.cc:543
        #12 0x7fff8478a5a9 in gpu::SharedImageStub::OnCreateSwapChain C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\shared_image_stub.cc:399
        #13 0x7fff84786f9a in gpu::SharedImageStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\shared_image_stub.cc:114
        #14 0x7fff80e0e3ef in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:709
        #15 0x7fff80e1cde0 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:970
        #16 0x7fff808299f6 in gpu::SchedulerDfs::ExecuteSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:763
        #17 0x7fff80827af4 in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:674
        #18 0x7fff8083038f in base::internal::Invoker<base::internal::BindState<void (gpu::SchedulerDfs::*)(),base::internal::UnretainedWrapper<gpu::SchedulerDfs,base::unretained_traits::MayNotDangle> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:970
        #19 0x7fff7c1a3567 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:165
        #20 0x7fff7f554257 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:489
        #21 0x7fff7f552d73 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:340
        #22 0x7fff7f523833 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:48
        #23 0x7fff7f556bc7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:649
        #24 0x7fff7c127141 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:140
        #25 0x7fff7ec5b2c1 in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc:399
        #26 0x7fff7a9abd93 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:760
        #27 0x7fff7a9aeaf4 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1122

    SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Image11.cpp:216 in rx::Image11::disassociateStorage
    Shadow bytes around the buggy address:
      0x120fcd16f600: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
      0x120fcd16f680: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
      0x120fcd16f700: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
      0x120fcd16f780: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
      0x120fcd16f800: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
    =>0x120fcd16f880:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
      0x120fcd16f900: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
      0x120fcd16f980: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
      0x120fcd16fa00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
      0x120fcd16fa80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
      0x120fcd16fb00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
    Shadow byte legend (one shadow byte represents 8 application bytes):
      Addressable:           00
      Partially addressable: 01 02 03 04 05 06 07
      Heap left redzone:       fa
      Freed heap region:       fd
      Stack left redzone:      f1
      Stack mid redzone:       f2
      Stack right redzone:     f3
      Stack after return:      f5
      Stack use after scope:   f8
      Global redzone:          f9
      Global init order:       f6
      Poisoned by user:        f7
      Container overflow:      fc
      Array cookie:            ac
      Intra object redzone:    bb
      ASan internal:           fe
      Left alloca redzone:     ca
      Right alloca redzone:    cb

    ==10188==ADDITIONAL INFO

    ==10188==Note: Please include this section with the ASan report.
    Task trace:
        #0 0x7fff80827d26 in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:690
        #1 0x7fff808210a2 in gpu::SchedulerDfs::TryScheduleSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:496


    MiraclePtr Status: NOT PROTECTED
    No raw_ptr<T> access to this region was detected prior to this crash.
    This crash is still exploitable with MiraclePtr.
    Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.


### [Deleted User] (2023-02-13)

[Empty comment from Monorail migration]

### vu...@sourcefire.com (2023-02-13)

[Comment Deleted]

### vu...@sourcefire.com (2023-02-13)

Advisory attached

### cl...@chromium.org (2023-02-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5343720571600896.

### cl...@chromium.org (2023-02-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-02-14)

ClusterFuzz testcase 5343720571600896 appears to be flaky, updating reproducibility label.

### ma...@google.com (2023-02-14)

I have not yet reproduced this issue. 

bajones@, could you assess this and route it to a good owner or work on a fix?


[Monorail components: Blink>WebGL]

### ka...@chromium.org (2023-02-14)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>ANGLE]

### ka...@chromium.org (2023-02-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-14)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-14)

[Empty comment from Monorail migration]

### ad...@google.com (2023-02-14)

(auto-cc on security bug)

### [Deleted User] (2023-02-27)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2023-03-08)

Security marshal here. geofflang@, could you confirm you intend to take a look at this, or if not, could you help re-triage?

### ge...@chromium.org (2023-03-08)

I can look this week.

### gi...@appspot.gserviceaccount.com (2023-03-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/a8720455fda43167465c3d2f9a13fca60c21f56e

commit a8720455fda43167465c3d2f9a13fca60c21f56e
Author: Geoff Lang <geofflang@chromium.org>
Date: Fri Mar 10 18:48:03 2023

D3D11: Add logic to disassociate EGL image storages.

The TextureStorage classes for External and EGLImages were missing the
logic to disassociate from images. This lead to the images continuing
to hold references to deleted storages.

Bug: chromium:1415330
Change-Id: I8303f6751d87a9b0a52993c7d4e9509b086b93f3
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4328347
Reviewed-by: Peng Huang <penghuang@chromium.org>
Commit-Queue: Geoff Lang <geofflang@chromium.org>

[modify] https://crrev.com/a8720455fda43167465c3d2f9a13fca60c21f56e/src/libANGLE/renderer/d3d/d3d11/TextureStorage11.cpp
[modify] https://crrev.com/a8720455fda43167465c3d2f9a13fca60c21f56e/src/libANGLE/renderer/d3d/d3d11/TextureStorage11.h
[modify] https://crrev.com/a8720455fda43167465c3d2f9a13fca60c21f56e/src/tests/gl_tests/ImageTest.cpp


### gi...@appspot.gserviceaccount.com (2023-03-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/87b71bd06d40407a8bfe4c8e4a60fa92ee51bba5

commit 87b71bd06d40407a8bfe4c8e4a60fa92ee51bba5
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Mar 15 00:51:50 2023

Roll ANGLE from 9c167fd21ed8 to 4982b903033b (2 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/9c167fd21ed8..4982b903033b

2023-03-14 cclao@google.com Revert "Vulkan: Remove inUseAndRespecifiedWithoutData from BufferVk"
2023-03-14 geofflang@chromium.org D3D11: Add logic to disassociate EGL image storages.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC angle-team@google.com,yuxinhu@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1415330
Tbr: yuxinhu@google.com
Change-Id: I4bdd229bda194cdaf641ea107948cfef685e90da
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4338539
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1117302}

[modify] https://crrev.com/87b71bd06d40407a8bfe4c8e4a60fa92ee51bba5/DEPS


### ge...@chromium.org (2023-03-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-16)

Requesting merge to extended stable M110 because latest trunk commit (1117302) appears to be after extended stable branch point (1084008).

Requesting merge to stable M111 because latest trunk commit (1117302) appears to be after stable branch point (1097615).

Requesting merge to beta M112 because latest trunk commit (1117302) appears to be after beta branch point (1109224).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [110, 111, 112].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2023-03-17)

merge approved for M110, M111! Please cherry-pick the fix to the appropriate branches by EOD PST today Friday, March 17 to get into the stable refreshes!

merge approved for M112! Please cherry-pick the fix to the appropriate branch by EOD PST Tuesday March 21st, to get into beta.


### gi...@appspot.gserviceaccount.com (2023-03-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/ce029c91a662f3ec991288bb689558fe4988ded7

commit ce029c91a662f3ec991288bb689558fe4988ded7
Author: Geoff Lang <geofflang@chromium.org>
Date: Fri Mar 10 18:48:03 2023

M110: D3D11: Add logic to disassociate EGL image storages.

The TextureStorage classes for External and EGLImages were missing the
logic to disassociate from images. This lead to the images continuing
to hold references to deleted storages.

Bug: chromium:1415330
Change-Id: I8303f6751d87a9b0a52993c7d4e9509b086b93f3
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4328347
Reviewed-by: Peng Huang <penghuang@chromium.org>
Commit-Queue: Geoff Lang <geofflang@chromium.org>
(cherry picked from commit a8720455fda43167465c3d2f9a13fca60c21f56e)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4348335
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/ce029c91a662f3ec991288bb689558fe4988ded7/src/libANGLE/renderer/d3d/d3d11/TextureStorage11.cpp
[modify] https://crrev.com/ce029c91a662f3ec991288bb689558fe4988ded7/src/libANGLE/renderer/d3d/d3d11/TextureStorage11.h


### gi...@appspot.gserviceaccount.com (2023-03-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/1d56a8f896c87cbb9daf2587c25d7ef76570c652

commit 1d56a8f896c87cbb9daf2587c25d7ef76570c652
Author: Geoff Lang <geofflang@chromium.org>
Date: Fri Mar 10 18:48:03 2023

M112: D3D11: Add logic to disassociate EGL image storages.

The TextureStorage classes for External and EGLImages were missing the
logic to disassociate from images. This lead to the images continuing
to hold references to deleted storages.

Bug: chromium:1415330
Change-Id: I8303f6751d87a9b0a52993c7d4e9509b086b93f3
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4328347
Reviewed-by: Peng Huang <penghuang@chromium.org>
Commit-Queue: Geoff Lang <geofflang@chromium.org>
(cherry picked from commit a8720455fda43167465c3d2f9a13fca60c21f56e)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4348337
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/1d56a8f896c87cbb9daf2587c25d7ef76570c652/src/libANGLE/renderer/d3d/d3d11/TextureStorage11.cpp
[modify] https://crrev.com/1d56a8f896c87cbb9daf2587c25d7ef76570c652/src/libANGLE/renderer/d3d/d3d11/TextureStorage11.h


### gi...@appspot.gserviceaccount.com (2023-03-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/1d56a8f896c87cbb9daf2587c25d7ef76570c652

commit 1d56a8f896c87cbb9daf2587c25d7ef76570c652
Author: Geoff Lang <geofflang@chromium.org>
Date: Fri Mar 10 18:48:03 2023

M112: D3D11: Add logic to disassociate EGL image storages.

The TextureStorage classes for External and EGLImages were missing the
logic to disassociate from images. This lead to the images continuing
to hold references to deleted storages.

Bug: chromium:1415330
Change-Id: I8303f6751d87a9b0a52993c7d4e9509b086b93f3
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4328347
Reviewed-by: Peng Huang <penghuang@chromium.org>
Commit-Queue: Geoff Lang <geofflang@chromium.org>
(cherry picked from commit a8720455fda43167465c3d2f9a13fca60c21f56e)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4348337
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/1d56a8f896c87cbb9daf2587c25d7ef76570c652/src/libANGLE/renderer/d3d/d3d11/TextureStorage11.cpp
[modify] https://crrev.com/1d56a8f896c87cbb9daf2587c25d7ef76570c652/src/libANGLE/renderer/d3d/d3d11/TextureStorage11.h


### ge...@chromium.org (2023-03-17)

I don't know why Git Watcher duplicated the M112 commits but I also merged to M111 here: https://chromium-review.googlesource.com/c/angle/angle/+/4348336

### pb...@google.com (2023-03-20)

Based on https://crbug.com/chromium/1415330#c28 dropping Merge-Approved-111.

### am...@chromium.org (2023-03-21)

[Empty comment from Monorail migration]

### pg...@google.com (2023-03-21)

[Empty comment from Monorail migration]

### pg...@google.com (2023-03-21)

[Empty comment from Monorail migration]

### vu...@sourcefire.com (2023-03-22)

 reward_to-piotr_at_thelead82.com

### am...@chromium.org (2023-03-22)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-22)

Congratulations, Piotr! The VRP Panel has decided to award you $15,000 for this report. Thank you for your efforts and reporting this issue to us -- great work! 

### am...@google.com (2023-03-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1415330?no_tracker_redirect=1

[Multiple monorail components: Blink>WebGL, Internals>GPU>ANGLE]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063051)*
