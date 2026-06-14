# Tab reliably crashing with STATUS_ACCESS_VIOLATION with reproduction steps

| Field | Value |
|-------|-------|
| **Issue ID** | [40059315](https://issues.chromium.org/issues/40059315) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | mi...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2022-04-07 |
| **Bounty** | $1,000.00 |

## Description

Chrome Version : 100.0.4896.75 (Official Build) (64-bit) (cohort: Stable)  

**URLs (if applicable) :** <https://jsbin.com/nowopiw/edit?html,css,output>  

**Other browsers tested:**  

Add OK or FAIL, along with the version, after other browsers where you  

**have tested this issue:**  

Edge: FAIL

**What steps will reproduce the problem?**  

**(1)** Open <https://jsbin.com/nowopiw/edit?html,css,output>  

**(2)** "Inspect Element" on the "I am some initial content" in the right side output  

**(3)** Toggle on grid debugging view by clicking the "grid" badge in DevTools "Elements" panel.  

(4) With DevTools still open, modify the jsbin HTML content by editing the text on the webpage in the jsbin HTML view panel on the left side.  

(5) Hover mouse over DevTools for tab crash with "Error code: STATUS\_ACCESS\_VIOLATION"  

(6) (In Edge browser, you can re-expand the iframe element in DevTools and see random/corrupted data briefly before crash)

**What is the expected result?**  

No crash, and DevTools correctly reflecting page content.

**What happens instead?**  

Tab crashes with "Error code: STATUS\_ACCESS\_VIOLATION"

Video of how to replicate crash is attached.

about:gpu:

Graphics Feature Status  

Canvas: Hardware accelerated  

Canvas out-of-process rasterization: Disabled  

Direct Rendering Display Compositor: Disabled  

Compositing: Hardware accelerated  

Multiple Raster Threads: Enabled  

OpenGL: Enabled  

Rasterization: Hardware accelerated  

Raw Draw: Disabled  

Skia Renderer: Enabled  

Video Decode: Hardware accelerated  

Video Encode: Hardware accelerated  

Vulkan: Disabled  

WebGL: Hardware accelerated  

WebGL2: Hardware accelerated  

Driver Bug Workarounds  

check\_ycbcr\_studio\_g22\_left\_p709\_for\_nv12\_support  

clear\_uniforms\_before\_first\_program\_use  

decode\_encode\_srgb\_for\_generatemipmap  

disable\_decode\_swap\_chain  

disable\_direct\_composition\_sw\_video\_overlays  

disable\_dynamic\_video\_encode\_framerate\_update  

enable\_bgra8\_overlays\_with\_yuv\_overlay\_support  

enable\_webgl\_timer\_query\_extensions  

exit\_on\_context\_lost  

max\_msaa\_sample\_count\_4  

msaa\_is\_slow  

no\_downscaled\_overlay\_promotion  

disabled\_extension\_GL\_KHR\_blend\_equation\_advanced  

disabled\_extension\_GL\_KHR\_blend\_equation\_advanced\_coherent  

Problems Detected  

Some drivers are unable to reset the D3D device in the GPU process sandbox  

Applied Workarounds: exit\_on\_context\_lost  

Clear uniforms before first program use on all platforms: 124764, 349137  

Applied Workarounds: clear\_uniforms\_before\_first\_program\_use  

On Intel GPUs MSAA performance is not acceptable for GPU rasterization: 527565  

Applied Workarounds: msaa\_is\_slow  

Disable KHR\_blend\_equation\_advanced until cc shaders are updated: 661715  

Applied Workarounds: disable(GL\_KHR\_blend\_equation\_advanced), disable(GL\_KHR\_blend\_equation\_advanced\_coherent)  

Decode and Encode before generateMipmap for srgb format textures on Windows: 634519  

Applied Workarounds: decode\_encode\_srgb\_for\_generatemipmap  

Expose WebGL's disjoint\_timer\_query extensions on platforms with site isolation: 808744, 870491  

Applied Workarounds: enable\_webgl\_timer\_query\_extensions  

Disable DecodeSwapChain for Intel Gen9 and older devices: 1107403  

Applied Workarounds: disable\_decode\_swap\_chain  

Intel GPUs fail to report BGRA8 overlay support: 1119491  

Applied Workarounds: enable\_bgra8\_overlays\_with\_yuv\_overlay\_support  

8x MSAA for WebGL contexts is slow on Win Intel: 1145793  

Applied Workarounds: max\_msaa\_sample\_count\_4  

Disable software overlays for Intel GPUs. All Skylake+ devices support hw overlays, older devices peform poorly.: 1192748  

Applied Workarounds: disable\_direct\_composition\_sw\_video\_overlays  

Check YCbCr\_Studio\_G22\_Left\_P709 color space for NV12 overlay support on Intel: 1103852  

Applied Workarounds: check\_ycbcr\_studio\_g22\_left\_p709\_for\_nv12\_support  

Intel GPUs do not promote downscaled overlays: 1245835  

Applied Workarounds: no\_downscaled\_overlay\_promotion  

AVC/AV1 hardware encoder MFT output bitrate incorrect upon framerate update on Intel GPUs.: 1295815  

Applied Workarounds: disable\_dynamic\_video\_encode\_framerate\_update  

ANGLE Features  

allow\_compressed\_formats (Frontend workarounds): Enabled: true  

Allow compressed formats  

disable\_anisotropic\_filtering (Frontend workarounds): Disabled  

Disable support for anisotropic filtering  

disable\_program\_binary (Frontend features) anglebug:5007: Disabled  

Disable support for GL\_OES\_get\_program\_binary  

disable\_program\_caching\_for\_transform\_feedback (Frontend workarounds): Disabled  

On some GPUs, program binaries don't contain transform feedback varyings  

enableCompressingPipelineCacheInThreadPool (Frontend workarounds) anglebug:4722: Disabled: false  

Enable compressing pipeline cache in thread pool.  

enableProgramBinaryForCapture (Frontend features) anglebug:5658: Disabled  

Even if FrameCapture is enabled, enable GL\_OES\_get\_program\_binary  

enable\_capture\_limits (Frontend features) anglebug:5750: Disabled  

Set the context limits like frame capturing was enabled  

forceInitShaderVariables (Frontend features): Disabled  

Force-enable shader variable initialization  

forceRobustResourceInit (Frontend features) anglebug:6041: Disabled  

Force-enable robust resource init  

lose\_context\_on\_out\_of\_memory (Frontend workarounds): Enabled: true  

Some users rely on a lost context notification if a GL\_OUT\_OF\_MEMORY error occurs  

scalarize\_vec\_and\_mat\_constructor\_args (Frontend workarounds) 1165751: Disabled: false  

Always rewrite vec/mat constructors to be consistent  

add\_mock\_texture\_no\_render\_target (D3D workarounds) anglebug:2152: Disabled: isIntel && capsVersion >= IntelDriverVersion(160000) && capsVersion < IntelDriverVersion(164815)  

On some drivers when rendering with no render target, two bugs lead to incorrect behavior  

allowES3OnFL10\_0 (D3D workarounds): Disabled: false  

Allow ES3 on 10.0 devices  

allow\_clear\_for\_robust\_resource\_init (D3D workarounds) 941620: Enabled: true  

Some drivers corrupt texture data when clearing for robust resource initialization.  

allow\_translate\_uniform\_block\_to\_structured\_buffer (D3D workarounds) anglebug:3682: Enabled: IsWin10OrGreater()  

There is a slow fxc compile performance issue with dynamic uniform indexing if translating a uniform block with a large array member to cbuffer.  

call\_clear\_twice (D3D workarounds) 655534: Disabled: isIntel && isSkylake && capsVersion >= IntelDriverVersion(160000) && capsVersion < IntelDriverVersion(164771)  

Using clear() may not take effect  

depth\_stencil\_blit\_extra\_copy (D3D workarounds) anglebug:1452: Disabled  

Bug in some drivers triggers a TDR when using CopySubresourceRegion from a staging texture to a depth/stencil  

disable\_b5g6r5\_support (D3D workarounds): Disabled: (isIntel && capsVersion >= IntelDriverVersion(150000) && capsVersion < IntelDriverVersion(154539)) || isAMD  

Textures with the format DXGI\_FORMAT\_B5G6R5\_UNORM have incorrect data  

emulate\_isnan\_float (D3D workarounds) 650547: Disabled: isIntel && isSkylake && capsVersion >= IntelDriverVersion(160000) && capsVersion < IntelDriverVersion(164542)  

Using isnan() on highp float will get wrong answer  

emulate\_tiny\_stencil\_textures (D3D workarounds): Disabled: isAMD && !(deviceCaps.featureLevel < D3D\_FEATURE\_LEVEL\_10\_1)  

1x1 and 2x2 mips of depth/stencil textures aren't sampled correctly  

expand\_integer\_pow\_expressions (D3D workarounds): Enabled: true  

The HLSL optimizer has a bug with optimizing 'pow' in certain integer-valued expressions  

flush\_after\_ending\_transform\_feedback (D3D workarounds): Disabled: isNvidia  

Some drivers sometimes write out-of-order results to StreamOut buffers when transform feedback is used to repeatedly write to the same buffer positions  

force\_atomic\_value\_resolution (D3D workarounds) anglebug:3246: Disabled: isNvidia  

On some drivers the return value from RWByteAddressBuffer.InterlockedAdd does not resolve when used in the .yzw components of a RWByteAddressBuffer.Store operation  

get\_dimensions\_ignores\_base\_level (D3D workarounds): Disabled: isNvidia  

Some drivers do not take into account the base level of the texture in the results of the HLSL GetDimensions builtin  

mrt\_perf\_workaround (D3D workarounds): Enabled: true  

Some drivers have a bug where they ignore null render targets  

pre\_add\_texel\_fetch\_offsets (D3D workarounds): Enabled: isIntel  

HLSL's function texture.Load returns 0 when the parameter Location is negative, even if the sum of Offset and Location is in range  

rewrite\_unary\_minus\_operator (D3D workarounds): Disabled: isIntel && (isBroadwell || isHaswell) && capsVersion >= IntelDriverVersion(150000) && capsVersion < IntelDriverVersion(154624)  

Evaluating unary minus operator on integer may get wrong answer in vertex shaders  

select\_view\_in\_geometry\_shader (D3D workarounds): Disabled: !deviceCaps.supportsVpRtIndexWriteFromVertexShader  

The viewport or render target slice will be selected in the geometry shader stage for the ANGLE\_multiview extension  

set\_data\_faster\_than\_image\_upload (D3D workarounds): Enabled: !(isIvyBridge || isBroadwell || isHaswell)  

Set data faster than image upload  

skip\_vs\_constant\_register\_zero (D3D workarounds): Disabled: isNvidia  

In specific cases the driver doesn't handle constant register zero correctly  

use\_instanced\_point\_sprite\_emulation (D3D workarounds): Disabled: isFeatureLevel9\_3  

Some D3D11 renderers do not support geometry shaders for pointsprite emulation  

use\_system\_memory\_for\_constant\_buffers (D3D workarounds) 593024: Enabled: isIntel  

Copying from staging storage to constant buffer storage does not work  

zero\_max\_lod (D3D workarounds): Disabled: isFeatureLevel9\_3  

Missing an option to disable mipmaps on a mipmapped texture  

DAWN Info

<Integrated GPU> D3D12 backend - Intel(R) UHD Graphics 630  

[Default Toggle Names]  

lazy\_clear\_resource\_on\_first\_use: <https://crbug.com/dawn/145>: Clears resource to zero on first usage. This initializes the resource so that no dirty bits from recycled memory is present in the new resource.  

use\_d3d12\_resource\_heap\_tier2: <https://crbug.com/dawn/27>: Enable support for resource heap tier 2. Resource heap tier 2 allows mixing of texture and buffers in the same heap. This allows better heap re-use and reduces fragmentation.  

use\_d3d12\_render\_pass: <https://crbug.com/dawn/36>: Use the D3D12 render pass API introduced in Windows build 1809 by default. On versions of Windows prior to build 1809, or when this toggle is turned off, Dawn will emulate a render pass.  

use\_d3d12\_residency\_management: <https://crbug.com/dawn/193>: Enable residency management. This allows page-in and page-out of resource heaps in GPU memory. This component improves overcommitted performance by keeping the most recently used resources local to the GPU. Turning this component off can cause allocation failures when application memory exceeds physical device memory.  

disallow\_unsafe\_apis: <http://crbug.com/1138528>: Produces validation errors on API entry points or parameter combinations that aren't considered secure yet.  

use\_temp\_buffer\_in\_small\_format\_texture\_to\_texture\_copy\_from\_greater\_to\_less\_mip\_level: <https://crbug.com/1161355>: Split texture-to-texture copy into two copies: copy from source texture into a temporary buffer, and copy from the temporary buffer into the destination texture under specific situations. This workaround is by default enabled on some Intel GPUs which have a driver bug in the execution of CopyTextureRegion() when we copy with the formats whose texel block sizes are less than 4 bytes from a greater mip level to a smaller mip level on D3D12 backends.  

[WebGPU Forced Toggles - enabled]  

disallow\_spirv: <https://crbug.com/1214923>: Disallow usage of SPIR-V completely so that only WGSL is used for shader modules.This is useful to prevent a Chromium renderer process from successfully sendingSPIR-V code to be compiled in the GPU process.  

[Supported Features]  

texture-compression-bc  

pipeline-statistics-query  

timestamp-query  

depth24unorm-stencil8  

depth32float-stencil8  

dawn-internal-usages  

multiplanar-formats  

dawn-native

<Discrete GPU> D3D12 backend - NVIDIA GeForce RTX 2080 with Max-Q Design  

[Default Toggle Names]  

lazy\_clear\_resource\_on\_first\_use: <https://crbug.com/dawn/145>: Clears resource to zero on first usage. This initializes the resource so that no dirty bits from recycled memory is present in the new resource.  

use\_d3d12\_resource\_heap\_tier2: <https://crbug.com/dawn/27>: Enable support for resource heap tier 2. Resource heap tier 2 allows mixing of texture and buffers in the same heap. This allows better heap re-use and reduces fragmentation.  

use\_d3d12\_render\_pass: <https://crbug.com/dawn/36>: Use the D3D12 render pass API introduced in Windows build 1809 by default. On versions of Windows prior to build 1809, or when this toggle is turned off, Dawn will emulate a render pass.  

use\_d3d12\_residency\_management: <https://crbug.com/dawn/193>: Enable residency management. This allows page-in and page-out of resource heaps in GPU memory. This component improves overcommitted performance by keeping the most recently used resources local to the GPU. Turning this component off can cause allocation failures when application memory exceeds physical device memory.  

disallow\_unsafe\_apis: <http://crbug.com/1138528>: Produces validation errors on API entry points or parameter combinations that aren't considered secure yet.  

[WebGPU Forced Toggles - enabled]  

disallow\_spirv: <https://crbug.com/1214923>: Disallow usage of SPIR-V completely so that only WGSL is used for shader modules.This is useful to prevent a Chromium renderer process from successfully sendingSPIR-V code to be compiled in the GPU process.  

[Supported Features]  

texture-compression-bc  

pipeline-statistics-query  

timestamp-query  

depth24unorm-stencil8  

depth32float-stencil8  

dawn-internal-usages  

multiplanar-formats  

dawn-native

<CPU> D3D12 backend - Microsoft Basic Render Driver  

[Default Toggle Names]  

lazy\_clear\_resource\_on\_first\_use: <https://crbug.com/dawn/145>: Clears resource to zero on first usage. This initializes the resource so that no dirty bits from recycled memory is present in the new resource.  

use\_d3d12\_resource\_heap\_tier2: <https://crbug.com/dawn/27>: Enable support for resource heap tier 2. Resource heap tier 2 allows mixing of texture and buffers in the same heap. This allows better heap re-use and reduces fragmentation.  

use\_d3d12\_render\_pass: <https://crbug.com/dawn/36>: Use the D3D12 render pass API introduced in Windows build 1809 by default. On versions of Windows prior to build 1809, or when this toggle is turned off, Dawn will emulate a render pass.  

use\_d3d12\_residency\_management: <https://crbug.com/dawn/193>: Enable residency management. This allows page-in and page-out of resource heaps in GPU memory. This component improves overcommitted performance by keeping the most recently used resources local to the GPU. Turning this component off can cause allocation failures when application memory exceeds physical device memory.  

disallow\_unsafe\_apis: <http://crbug.com/1138528>: Produces validation errors on API entry points or parameter combinations that aren't considered secure yet.  

[WebGPU Forced Toggles - enabled]  

disallow\_spirv: <https://crbug.com/1214923>: Disallow usage of SPIR-V completely so that only WGSL is used for shader modules.This is useful to prevent a Chromium renderer process from successfully sendingSPIR-V code to be compiled in the GPU process.  

[Supported Features]  

texture-compression-bc  

pipeline-statistics-query  

timestamp-query  

depth24unorm-stencil8  

depth32float-stencil8  

dawn-internal-usages  

multiplanar-formats  

dawn-native

<Integrated GPU> Vulkan backend - Intel(R) UHD Graphics 630  

[Default Toggle Names]  

lazy\_clear\_resource\_on\_first\_use: <https://crbug.com/dawn/145>: Clears resource to zero on first usage. This initializes the resource so that no dirty bits from recycled memory is present in the new resource.  

use\_temporary\_buffer\_in\_texture\_to\_texture\_copy: <https://crbug.com/dawn/42>: Split texture-to-texture copy into two copies: copy from source texture into a temporary buffer, and copy from the temporary buffer into the destination texture when copying between compressed textures that don't have block-aligned sizes. This workaround is enabled by default on all Vulkan drivers to solve an issue in the Vulkan SPEC about the texture-to-texture copies with compressed formats. See #1005 (<https://github.com/KhronosGroup/Vulkan-Docs/issues/1005>) for more details.  

vulkan\_use\_d32s8: <https://crbug.com/dawn/286>: Vulkan mandates support of either D32\_FLOAT\_S8 or D24\_UNORM\_S8. When available the backend will use D32S8 (toggle to on) but setting the toggle to off will make it use the D24S8 format when possible.  

disallow\_unsafe\_apis: <http://crbug.com/1138528>: Produces validation errors on API entry points or parameter combinations that aren't considered secure yet.  

[WebGPU Forced Toggles - enabled]  

disallow\_spirv: <https://crbug.com/1214923>: Disallow usage of SPIR-V completely so that only WGSL is used for shader modules.This is useful to prevent a Chromium renderer process from successfully sendingSPIR-V code to be compiled in the GPU process.  

[Supported Features]  

texture-compression-bc  

texture-compression-etc2  

texture-compression-astc  

pipeline-statistics-query  

timestamp-query  

depth-clamping  

depth24unorm-stencil8  

depth32float-stencil8  

dawn-internal-usages  

dawn-native

<Discrete GPU> Vulkan backend - NVIDIA GeForce RTX 2080 with Max-Q Design  

[Default Toggle Names]  

lazy\_clear\_resource\_on\_first\_use: <https://crbug.com/dawn/145>: Clears resource to zero on first usage. This initializes the resource so that no dirty bits from recycled memory is present in the new resource.  

use\_temporary\_buffer\_in\_texture\_to\_texture\_copy: <https://crbug.com/dawn/42>: Split texture-to-texture copy into two copies: copy from source texture into a temporary buffer, and copy from the temporary buffer into the destination texture when copying between compressed textures that don't have block-aligned sizes. This workaround is enabled by default on all Vulkan drivers to solve an issue in the Vulkan SPEC about the texture-to-texture copies with compressed formats. See #1005 (<https://github.com/KhronosGroup/Vulkan-Docs/issues/1005>) for more details.  

vulkan\_use\_d32s8: <https://crbug.com/dawn/286>: Vulkan mandates support of either D32\_FLOAT\_S8 or D24\_UNORM\_S8. When available the backend will use D32S8 (toggle to on) but setting the toggle to off will make it use the D24S8 format when possible.  

disallow\_unsafe\_apis: <http://crbug.com/1138528>: Produces validation errors on API entry points or parameter combinations that aren't considered secure yet.  

[WebGPU Forced Toggles - enabled]  

disallow\_spirv: <https://crbug.com/1214923>: Disallow usage of SPIR-V completely so that only WGSL is used for shader modules.This is useful to prevent a Chromium renderer process from successfully sendingSPIR-V code to be compiled in the GPU process.  

[Supported Features]  

texture-compression-bc  

pipeline-statistics-query  

timestamp-query  

depth-clamping  

depth24unorm-stencil8  

depth32float-stencil8  

dawn-internal-usages  

dawn-native

<CPU> Vulkan backend - SwiftShader Device (Subzero)  

[Default Toggle Names]  

lazy\_clear\_resource\_on\_first\_use: <https://crbug.com/dawn/145>: Clears resource to zero on first usage. This initializes the resource so that no dirty bits from recycled memory is present in the new resource.  

use\_temporary\_buffer\_in\_texture\_to\_texture\_copy: <https://crbug.com/dawn/42>: Split texture-to-texture copy into two copies: copy from source texture into a temporary buffer, and copy from the temporary buffer into the destination texture when copying between compressed textures that don't have block-aligned sizes. This workaround is enabled by default on all Vulkan drivers to solve an issue in the Vulkan SPEC about the texture-to-texture copies with compressed formats. See #1005 (<https://github.com/KhronosGroup/Vulkan-Docs/issues/1005>) for more details.  

vulkan\_use\_d32s8: <https://crbug.com/dawn/286>: Vulkan mandates support of either D32\_FLOAT\_S8 or D24\_UNORM\_S8. When available the backend will use D32S8 (toggle to on) but setting the toggle to off will make it use the D24S8 format when possible.  

disallow\_unsafe\_apis: <http://crbug.com/1138528>: Produces validation errors on API entry points or parameter combinations that aren't considered secure yet.  

[WebGPU Forced Toggles - enabled]  

disallow\_spirv: <https://crbug.com/1214923>: Disallow usage of SPIR-V completely so that only WGSL is used for shader modules.This is useful to prevent a Chromium renderer process from successfully sendingSPIR-V code to be compiled in the GPU process.  

[Supported Features]  

texture-compression-bc  

texture-compression-etc2  

texture-compression-astc  

timestamp-query  

depth-clamping  

depth32float-stencil8  

dawn-internal-usages  

dawn-native  

Version Information  

Data exported 2022-04-07T14:03:03.568Z  

Chrome version Chrome/100.0.4896.75  

Operating system Windows NT 10.0.22000  

Software rendering list URL <https://chromium.googlesource.com/chromium/src/+/d9568d04d7dd79269c5a655d7ada69650c5a8336/gpu/config/software_rendering_list.json>  

Driver bug list URL <https://chromium.googlesource.com/chromium/src/+/d9568d04d7dd79269c5a655d7ada69650c5a8336/gpu/config/gpu_driver_bug_list.json>  

ANGLE commit id cc8b741c6ba4  

2D graphics backend Skia/100 65809fe1d0d63215f6f25fb38f869f878b09c700  

Command Line "C:\Program Files\Google\Chrome\Application\chrome.exe" --origin-trial-disabled-features=ConditionalFocus --profile-directory="Profile 1" --flag-switches-begin --flag-switches-end  

Driver Information  

Initialization time 218  

In-process GPU false  

Passthrough Command Decoder true  

Sandboxed true  

GPU0 VENDOR= 0x8086, DEVICE=0x3e9b, SUBSYS=0x20061a58, LUID={0,59958} \*ACTIVE\*  

GPU1 VENDOR= 0x10de, DEVICE=0x1e90, SUBSYS=0x20051a58, REV=161, LUID={0,60688}  

GPU2 VENDOR= 0x1414, DEVICE=0x008c, LUID={0,60618}  

Optimus false  

AMD switchable false  

Desktop compositing Aero Glass  

Direct composition true  

Supports overlays true  

YUY2 overlay support DIRECT  

NV12 overlay support DIRECT  

BGRA8 overlay support DIRECT  

RGB10A2 overlay support SOFTWARE  

Driver D3D12 feature level D3D 12.1  

Driver Vulkan API version Vulkan API 1.3.0  

Driver vendor Intel  

Driver version 26.20.100.7261  

GPU CUDA compute capability major version 0  

Pixel shader version 5.0  

Vertex shader version 5.0  

Max. MSAA samples 16  

Machine model name  

Machine model version  

GL\_VENDOR Google Inc. (Intel)  

GL\_RENDERER ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs\_5\_0 ps\_5\_0, D3D11-26.20.100.7261)  

GL\_VERSION OpenGL ES 2.0.0 (ANGLE 2.1.17981 git hash: cc8b741c6ba4)  

GL\_EXTENSIONS GL\_ANGLE\_base\_vertex\_base\_instance GL\_ANGLE\_base\_vertex\_base\_instance\_shader\_builtin GL\_ANGLE\_client\_arrays GL\_ANGLE\_depth\_texture GL\_ANGLE\_framebuffer\_blit GL\_ANGLE\_framebuffer\_multisample GL\_ANGLE\_get\_serialized\_context\_string GL\_ANGLE\_get\_tex\_level\_parameter GL\_ANGLE\_instanced\_arrays GL\_ANGLE\_lossy\_etc\_decode GL\_ANGLE\_memory\_size GL\_ANGLE\_multi\_draw GL\_ANGLE\_pack\_reverse\_row\_order GL\_ANGLE\_program\_cache\_control GL\_ANGLE\_provoking\_vertex GL\_ANGLE\_request\_extension GL\_ANGLE\_robust\_client\_memory GL\_ANGLE\_texture\_compression\_dxt3 GL\_ANGLE\_texture\_compression\_dxt5 GL\_ANGLE\_texture\_usage GL\_ANGLE\_translated\_shader\_source GL\_CHROMIUM\_bind\_generates\_resource GL\_CHROMIUM\_bind\_uniform\_location GL\_CHROMIUM\_color\_buffer\_float\_rgb GL\_CHROMIUM\_color\_buffer\_float\_rgba GL\_CHROMIUM\_copy\_compressed\_texture GL\_CHROMIUM\_copy\_texture GL\_CHROMIUM\_lose\_context GL\_CHROMIUM\_sync\_query GL\_EXT\_EGL\_image\_external\_wrap\_modes GL\_EXT\_blend\_func\_extended GL\_EXT\_blend\_minmax GL\_EXT\_clip\_control GL\_EXT\_color\_buffer\_half\_float GL\_EXT\_debug\_label GL\_EXT\_debug\_marker GL\_EXT\_discard\_framebuffer GL\_EXT\_disjoint\_timer\_query GL\_EXT\_draw\_buffers GL\_EXT\_draw\_elements\_base\_vertex GL\_EXT\_float\_blend GL\_EXT\_frag\_depth GL\_EXT\_instanced\_arrays GL\_EXT\_map\_buffer\_range GL\_EXT\_multi\_draw\_indirect GL\_EXT\_multisampled\_render\_to\_texture GL\_EXT\_occlusion\_query\_boolean GL\_EXT\_read\_format\_bgra GL\_EXT\_robustness GL\_EXT\_sRGB GL\_EXT\_shader\_texture\_lod GL\_EXT\_texture\_compression\_bptc GL\_EXT\_texture\_compression\_dxt1 GL\_EXT\_texture\_compression\_rgtc GL\_EXT\_texture\_compression\_s3tc\_srgb GL\_EXT\_texture\_filter\_anisotropic GL\_EXT\_texture\_format\_BGRA8888 GL\_EXT\_texture\_rg GL\_EXT\_texture\_storage GL\_EXT\_unpack\_subimage GL\_KHR\_debug GL\_KHR\_parallel\_shader\_compile GL\_NV\_EGL\_stream\_consumer\_external GL\_NV\_fence GL\_NV\_framebuffer\_blit GL\_NV\_pack\_subimage GL\_NV\_pixel\_buffer\_object GL\_OES\_EGL\_image GL\_OES\_EGL\_image\_external GL\_OES\_compressed\_EAC\_R11\_signed\_texture GL\_OES\_compressed\_EAC\_R11\_unsigned\_texture GL\_OES\_compressed\_EAC\_RG11\_signed\_texture GL\_OES\_compressed\_EAC\_RG11\_unsigned\_texture GL\_OES\_compressed\_ETC2\_RGB8\_texture GL\_OES\_compressed\_ETC2\_RGBA8\_texture GL\_OES\_compressed\_ETC2\_punchthroughA\_RGBA8\_texture GL\_OES\_compressed\_ETC2\_punchthroughA\_sRGB8\_alpha\_texture GL\_OES\_compressed\_ETC2\_sRGB8\_alpha8\_texture GL\_OES\_compressed\_ETC2\_sRGB8\_texture GL\_OES\_depth24 GL\_OES\_depth32 GL\_OES\_draw\_elements\_base\_vertex GL\_OES\_element\_index\_uint GL\_OES\_fbo\_render\_mipmap GL\_OES\_get\_program\_binary GL\_OES\_mapbuffer GL\_OES\_packed\_depth\_stencil GL\_OES\_rgb8\_rgba8 GL\_OES\_standard\_derivatives GL\_OES\_surfaceless\_context GL\_OES\_texture\_border\_clamp GL\_OES\_texture\_float GL\_OES\_texture\_float\_linear GL\_OES\_texture\_half\_float GL\_OES\_texture\_half\_float\_linear GL\_OES\_texture\_npot GL\_OES\_texture\_stencil8 GL\_OES\_vertex\_array\_object GL\_WEBGL\_video\_texture  

Disabled Extensions GL\_KHR\_blend\_equation\_advanced GL\_KHR\_blend\_equation\_advanced\_coherent  

Disabled WebGL Extensions  

Window system binding vendor Google Inc. (Intel)  

Window system binding version 1.5 (ANGLE 2.1.17981 git hash: cc8b741c6ba4)  

Window system binding extensions EGL\_EXT\_create\_context\_robustness EGL\_ANGLE\_d3d\_share\_handle\_client\_buffer EGL\_ANGLE\_d3d\_texture\_client\_buffer EGL\_ANGLE\_surface\_d3d\_texture\_2d\_share\_handle EGL\_ANGLE\_query\_surface\_pointer EGL\_ANGLE\_window\_fixed\_size EGL\_ANGLE\_keyed\_mutex EGL\_ANGLE\_surface\_orientation EGL\_ANGLE\_direct\_composition EGL\_NV\_post\_sub\_buffer EGL\_KHR\_create\_context EGL\_KHR\_image EGL\_KHR\_image\_base EGL\_KHR\_gl\_texture\_2D\_image EGL\_KHR\_gl\_texture\_cubemap\_image EGL\_KHR\_gl\_renderbuffer\_image EGL\_KHR\_get\_all\_proc\_addresses EGL\_KHR\_stream EGL\_KHR\_stream\_consumer\_gltexture EGL\_NV\_stream\_consumer\_gltexture\_yuv EGL\_ANGLE\_stream\_producer\_d3d\_texture EGL\_ANGLE\_create\_context\_webgl\_compatibility EGL\_CHROMIUM\_create\_context\_bind\_generates\_resource EGL\_CHROMIUM\_sync\_control EGL\_EXT\_pixel\_format\_float EGL\_KHR\_surfaceless\_context EGL\_ANGLE\_display\_texture\_share\_group EGL\_ANGLE\_display\_semaphore\_share\_group EGL\_ANGLE\_create\_context\_client\_arrays EGL\_ANGLE\_program\_cache\_control EGL\_ANGLE\_robust\_resource\_initialization EGL\_ANGLE\_create\_context\_extensions\_enabled EGL\_ANDROID\_blob\_cache EGL\_ANDROID\_recordable EGL\_ANGLE\_image\_d3d11\_texture EGL\_ANGLE\_create\_context\_backwards\_compatible EGL\_KHR\_no\_config\_context EGL\_KHR\_create\_context\_no\_error EGL\_KHR\_reusable\_sync EGL\_KHR\_mutable\_render\_buffer  

Direct rendering version unknown  

Reset notification strategy 0x8252  

GPU process crash count 0  

gfx::BufferFormats supported for allocation and texturing R\_8: not supported, R\_16: not supported, RG\_88: not supported, RG\_1616: not supported, BGR\_565: not supported, RGBA\_4444: not supported, RGBX\_8888: not supported, RGBA\_8888: not supported, BGRX\_8888: not supported, BGRA\_1010102: not supported, RGBA\_1010102: not supported, BGRA\_8888: not supported, RGBA\_F16: not supported, YVU\_420: not supported, YUV\_420\_BIPLANAR: not supported, P010: not supported  

Compositor Information  

Tile Update Mode One-copy  

Partial Raster Enabled  

GpuMemoryBuffers Status  

R\_8 Software only  

R\_16 Software only  

RG\_88 Software only  

RG\_1616 Software only  

BGR\_565 Software only  

RGBA\_4444 Software only  

RGBX\_8888 GPU\_READ, SCANOUT  

RGBA\_8888 GPU\_READ, SCANOUT  

BGRX\_8888 Software only  

BGRA\_1010102 Software only  

RGBA\_1010102 Software only  

BGRA\_8888 Software only  

RGBA\_F16 Software only  

YVU\_420 Software only  

YUV\_420\_BIPLANAR GPU\_READ, SCANOUT  

P010 Software only  

Display(s) Information  

Info Display[2528732444] bounds=[0,0 2560x1440], workarea=[0,0 2560x1392], scale=1.5, rotation=0, panel\_rotation=0 internal.  

Color space (sRGB/no-alpha) {primaries:BT709, transfer:SRGB, matrix:RGB, range:FULL}  

Buffer format (sRGB/no-alpha) BGRX\_8888  

Color space (sRGB/alpha) {primaries:BT709, transfer:SRGB, matrix:RGB, range:FULL}  

Buffer format (sRGB/alpha) BGRA\_8888  

Color space (WCG/no-alpha) {primaries:BT709, transfer:SRGB, matrix:RGB, range:FULL}  

Buffer format (WCG/no-alpha) BGRX\_8888  

Color space (WCG/alpha) {primaries:BT709, transfer:SRGB, matrix:RGB, range:FULL}  

Buffer format (WCG/alpha) BGRA\_8888  

Color space (HDR/no-alpha) {primaries:BT709, transfer:SRGB, matrix:RGB, range:FULL}  

Buffer format (HDR/no-alpha) BGRX\_8888  

Color space (HDR/alpha) {primaries:BT709, transfer:SRGB, matrix:RGB, range:FULL}  

Buffer format (HDR/alpha) BGRA\_8888  

SDR white level in nits 80  

HDR relative maximum luminance 1  

Bits per color component 8  

Bits per pixel 24  

Refresh Rate in Hz 60  

Video Acceleration Information  

Decoding (VideoDecoder)  

Decode h264 baseline 64x64 to 4096x4096 pixels  

Decode h264 main 64x64 to 4096x4096 pixels  

Decode h264 high 64x64 to 4096x4096 pixels  

Decode vp9 profile0 64x64 to 8192x8192 pixels  

Decode vp9 profile2 64x64 to 8192x8192 pixels  

Decoding (Legacy VideoDecodeAccelerator)  

Decode h264 baseline 64x64 to 4096x4096 pixels  

Decode h264 main 64x64 to 4096x4096 pixels  

Decode h264 high 64x64 to 4096x4096 pixels  

Decode vp9 profile0 64x64 to 8192x8192 pixels  

Decode vp9 profile2 64x64 to 8192x8192 pixels  

Encoding  

Encode h264 baseline 0x0 to 1920x1088 pixels, and/or 30.000 fps  

Encode h264 main 0x0 to 1920x1088 pixels, and/or 30.000 fps  

Encode h264 high 0x0 to 1920x1088 pixels, and/or 30.000 fps  

Vulkan Information  

Device Performance Information  

Total Physical Memory (Gb) 15  

Total Disk Space (Gb) 930  

Hardware Concurrency 12  

System Commit Limit (Gb) 22  

D3D11 Feature Level 12\_1  

Has Discrete GPU yes  

Intel GPU Generation 9  

Software Rendering No  

Diagnostics  

Log Messages  

GpuProcessHost: The info collection GPU process exited normally. Everything is okay.

## Attachments

- [out.mp4](attachments/out.mp4) (video/mp4, 247.4 KB)
- [1314310.mp4](attachments/1314310.mp4) (video/mp4, 2.9 MB)

## Timeline

### dt...@chromium.org (2022-04-07)

Can you provide the server crash report ID from chrome://crashes?

### jh...@chromium.org (2022-04-08)

[Empty comment from Monorail migration]

### mi...@gmail.com (2022-04-09)

Uploaded Crash Report ID:	6c63fcf330dd9d11
Upload Time:	Saturday, April 9, 2022 at 5:44:33 PM

### [Deleted User] (2022-04-09)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2022-04-11)

[Empty comment from Monorail migration]

[Monorail components: Blink>HTML]

### de...@chromium.org (2022-04-11)

Able to reproduce the issue on chrome version #100.0.4896.75 using Windows 11,Mac 12.3, Linux Debian by the following steps as per https://crbug.com/chromium/1314310#c0.

Reproducible on
================
102.0.4996.0- Canary
102.0.4987.0- Dev 
101.0.4951.26- Beta  
100.0.4896.75- Stable

Attaching screencast for reference.
The same issue seems to be reproducible from M-89 older versions, hence considering it as Non-Regression and marking it as untriaged.

### dt...@chromium.org (2022-04-11)

[Empty comment from Monorail migration]

[Monorail components: -Blink>HTML Blink>DOM Platform>DevTools]

### ja...@chromium.org (2022-04-11)

Maybe this is something to do with dgrogan's recent work with DevTools layout information?

[Monorail components: -Blink>DOM Blink>Layout>Grid]

### ik...@chromium.org (2022-04-11)

This doesn't appear to be directly layout related - based on the crash its likely devtools accessing a document which has been cleared out.

[Monorail components: -Blink>Layout>Grid]

### dg...@chromium.org (2022-04-11)

Unlikely to be related to Layout->DevTools stuff, given https://crbug.com/chromium/1314310#c6:

> The same issue seems to be reproducible from M-89 older versions

https://crash.corp.google.com/browse?q=&stbtiq=product:Chrome%206c63fcf330dd9d11&reportid=6c63fcf330dd9d11&index=0#4

### dg...@chromium.org (2022-04-11)

+brgoddar, who looks like originally wrote the multi-grid highlighter, for triage

### dg...@chromium.org (2022-04-11)

+patrick for triage, since brgoddar seems to be gone

### dl...@gmail.com (2022-04-11)

alexrudenko@ - the Member<Node> pointers in the Vector<std::pair>'s of PersistentTool are not going to be traced. PersistentTool should either be put on the oilpan heap or use Persistent<Node> (both raise questions about keeping large object graphs alive longer than is appropriate, but former generally seems better than the latter).

Can you take a look?

0faab6de7c1a55 (Alex Rudenko       2021-03-31 09:41:26 +0000 149) using GridConfigs = Vector<
485303a0695aef (Alex Rudenko       2020-11-17 10:18:37 +0000 150)     std::pair<Member<Node>, std::unique_ptr<InspectorGridHighlightConfig>>>;
485303a0695aef (Alex Rudenko       2020-11-17 10:18:37 +0000 151) using FlexContainerConfigs =
485303a0695aef (Alex Rudenko       2020-11-17 10:18:37 +0000 152)     Vector<std::pair<Member<Node>,
485303a0695aef (Alex Rudenko       2020-11-17 10:18:37 +0000 153)                      std::unique_ptr<InspectorFlexContainerHighlightConfig>>>;

cc leolee@ as brgoddar@ is no longer working on DevTools

### dt...@chromium.org (2022-04-11)

Untraced member first occurred in https://chromium-review.googlesource.com/c/chromium/src/+/2278408

### [Deleted User] (2022-04-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-11)

[Empty comment from Monorail migration]

### pa...@microsoft.com (2022-04-12)

I unfortunately no longer work on DevTools code at the moment, but what ikilpatrick said in https://crbug.com/chromium/1314310#c9 is most likely what is happening here.
Hopefully Alex Rudenko can investigate this issue. Leo Lee is also cc'd here and can probably find somebody to investigate as well.

### dc...@chromium.org (2022-04-14)

Untraced Oilpan objects are a memory safety issue that must be fixed ASAP.

alexrudenko@ is marked OOO so assigning to caseq@. I have also filed https://crbug.com/chromium/1316469 for improving the Oilpan plugin to proactively catch this sort of issue going forward.

### ml...@chromium.org (2022-04-15)

Does the fact that this requires user interaction (opening DevTools) have an impact on the severity?

### ml...@chromium.org (2022-04-15)

[Empty comment from Monorail migration]

### al...@chromium.org (2022-04-19)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2e0a0b83e1340e948a27cdc319bea8f32849d414

commit 2e0a0b83e1340e948a27cdc319bea8f32849d414
Author: Alex Rudenko <alexrudenko@chromium.org>
Date: Thu Apr 21 20:03:06 2022

DevTools: store weak references to nodes in inspect_tools

This CL changes how the configuration for persistent overlays is stored.
Instead of trying to save a strong reference to a DOM node, we can
store weak references instead. This requires using a HeapHashMap as
vectors don't support weak reference elements.

Fixed: 1314310
Change-Id: I27ce12730d7598bc84d01adf421923af9a53dc67
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3593092
Reviewed-by: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Changhao Han <changhaohan@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Commit-Queue: Alex Rudenko <alexrudenko@chromium.org>
Cr-Commit-Position: refs/heads/main@{#994866}

[modify] https://crrev.com/2e0a0b83e1340e948a27cdc319bea8f32849d414/third_party/blink/renderer/core/inspector/inspector_highlight.cc
[modify] https://crrev.com/2e0a0b83e1340e948a27cdc319bea8f32849d414/third_party/blink/renderer/core/inspector/inspect_tools.h
[modify] https://crrev.com/2e0a0b83e1340e948a27cdc319bea8f32849d414/third_party/blink/renderer/core/inspector/inspector_overlay_agent.h
[modify] https://crrev.com/2e0a0b83e1340e948a27cdc319bea8f32849d414/third_party/blink/renderer/core/inspector/inspector_overlay_agent.cc
[modify] https://crrev.com/2e0a0b83e1340e948a27cdc319bea8f32849d414/third_party/blink/renderer/core/inspector/inspect_tools.cc
[modify] https://crrev.com/2e0a0b83e1340e948a27cdc319bea8f32849d414/third_party/blink/renderer/core/inspector/inspector_highlight.h


### [Deleted User] (2022-04-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-22)

Requesting merge to dev M102 because latest trunk commit (994866) appears to be after dev branch point (992738).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-22)

Merge approved: your change passed merge requirements and is auto-approved for M102. Please go ahead and merge the CL to branch 5005 (refs/branch-heads/5005) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-04-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/919b1ffe1fe75aa7f77213c0291e6396a6a60e43

commit 919b1ffe1fe75aa7f77213c0291e6396a6a60e43
Author: Alex Rudenko <alexrudenko@chromium.org>
Date: Tue Apr 26 05:53:56 2022

[M102] DevTools: store weak references to nodes in inspect_tools

This CL changes how the configuration for persistent overlays is stored.
Instead of trying to save a strong reference to a DOM node, we can
store weak references instead. This requires using a HeapHashMap as
vectors don't support weak reference elements.

(cherry picked from commit 2e0a0b83e1340e948a27cdc319bea8f32849d414)

Fixed: 1314310
Change-Id: I27ce12730d7598bc84d01adf421923af9a53dc67
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3593092
Reviewed-by: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Changhao Han <changhaohan@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Commit-Queue: Alex Rudenko <alexrudenko@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#994866}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3604262
Auto-Submit: Alex Rudenko <alexrudenko@chromium.org>
Reviewed-by: Simon Zünd <szuend@chromium.org>
Commit-Queue: Simon Zünd <szuend@chromium.org>
Cr-Commit-Position: refs/branch-heads/5005@{#163}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/919b1ffe1fe75aa7f77213c0291e6396a6a60e43/third_party/blink/renderer/core/inspector/inspect_tools.h
[modify] https://crrev.com/919b1ffe1fe75aa7f77213c0291e6396a6a60e43/third_party/blink/renderer/core/inspector/inspector_highlight.cc
[modify] https://crrev.com/919b1ffe1fe75aa7f77213c0291e6396a6a60e43/third_party/blink/renderer/core/inspector/inspector_overlay_agent.h
[modify] https://crrev.com/919b1ffe1fe75aa7f77213c0291e6396a6a60e43/third_party/blink/renderer/core/inspector/inspector_overlay_agent.cc
[modify] https://crrev.com/919b1ffe1fe75aa7f77213c0291e6396a6a60e43/third_party/blink/renderer/core/inspector/inspect_tools.cc
[modify] https://crrev.com/919b1ffe1fe75aa7f77213c0291e6396a6a60e43/third_party/blink/renderer/core/inspector/inspector_highlight.h


### am...@google.com (2022-04-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-28)

Hello, thank you for reporting this issue that ended up having security implications. For that, the Chrome VRP would like to extend to you a $1,000 thank you reward. A member of our finance team will soon be in touch to arrange payment. Please also let us know by what name/handle/tag you would like to be acknowledged for this issue. Thanks again for reporting this issue to us! 

### am...@google.com (2022-05-07)

[Empty comment from Monorail migration]

### mi...@gmail.com (2022-05-23)

I would be honored to accept the reward and have replied to the email from the VRP team :)

My online alias/handle/tag is EllisVlad

### am...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### dg...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1314310?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059315)*
