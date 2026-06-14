# REGRESSION: Memory corruption in open source JPEG decoder (r61619)

| Field | Value |
|-------|-------|
| **Issue ID** | [40081931](https://issues.chromium.org/issues/40081931) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ao...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2010-07-01 |
| **Bounty** | $500.00 |

## Description

A renderer segmentation fault occurs, caused by EIP being 0 below WebCore::JPEGImageReader::decode, when the attached JPEG image is displayed on a page. This happens at least in Chromium (6.0.452.0 (Developer Build 51212) Ubuntu 10.04) on x86 and x86_64. Current Google Chrome does not seem to be affected. Not tested on other platforms.

Backtrace begins:
Program received signal SIGSEGV, Segmentation fault.
0x00000000 in ?? ()
(gdb) bt
#0  0x00000000 in ?? ()
#1  0x0903ffe8 in WebCore::JPEGImageReader::decode (this=0xa6c1040, data=..., 
    onlySize=true)
    at third_party/WebKit/WebCore/platform/image-decoders/jpeg/JPEGImageDecodercpp:213
#2  0x0904047b in WebCore::JPEGImageDecoder::decode (this=0xa6caa50, 
    onlySize=true)
    at third_party/WebKit/WebCore/platform/image-decoders/jpeg/JPEGImageDecodercpp:487
#3  0x09040656 in WebCore::JPEGImageDecoder::isSizeAvailable (this=0xa6caa50)
    at third_party/WebKit/WebCore/platform/image-decoders/jpeg/JPEGImageDecodercpp:375
#4  0x09023670 in WebCore::BitmapImage::isSizeAvailable (this=0xa64e120)
    at third_party/WebKit/WebCore/platform/graphics/BitmapImage.cpp:202
#5  0x08f83bcc in WebCore::CachedImage::data (this=0xa6be000, data=..., 
    allDataReceived=<value optimized out>)
    at third_party/WebKit/WebCore/loader/CachedImage.cpp:275
#6  0x09291015 in WebCore::ImageDocumentParser::appendBytes (this=0xa618830)
    at third_party/WebKit/WebCore/loader/ImageDocument.cpp:129
#7  0x08f964f1 in WebCore::DocumentWriter::addData (this=0xa663d50, 
    str=0xb6b86000 "\377\330\377", <incomplete sequence \340>, len=347, 
    flush=false) at third_party/WebKit/WebCore/loader/DocumentWriter.cpp:200
#8  0x08f993ec in WebCore::FrameLoader::addData (this=0xa663c28, 
[...]

## Attachments

- [segv.jpeg](attachments/segv.jpeg) (image/jpeg, 347 B)

## Timeline

### in...@chromium.org (2010-07-01)

Most times, it crashes on a null deref. but like one in 6 six times, you will see the m_decoder gets junk values after the setsize with big width and height values. i checked closely and i can definitely see a USE AFTER FREE vulnerability. Affect

d:\chromium\src\third_party\WebKit\WebCore\platform\image-decoders\jpeg\JPEGImageDecoder.cpp
            if (!m_decoder->setSize(m_info.image_width, m_info.image_height))
                return m_decoder->setFailed(); 

the fix looks to be removing the extra setfailed call in 
        virtual bool setSize(unsigned width, unsigned height)
        {
            if (isOverSize(width, height))
                return setFailed();
// change setfailed to false; since setfailed is already called at the jpeg decoder level.

ccing Peter for comments.

Does not affect v5 chrome stable. But crashes v5 stable safari, v6 chromium trunk.

### pk...@chromium.org (2010-07-01)

The correct fix is to change JPEGImageDecoder.cpp:213 from "return m_decoder->setFailed();" to "return false;".

Safari does not use this file, so if Safari crashes in your tests it's due to a different bug.

This hasn't shipped to anywhere other than Dev channel.

### in...@chromium.org (2010-07-01)

Yes, i was just writing a comment on that. I do see some more places vulnerable, which i will fix as well. filing a webkit bug and working on it.

### in...@chromium.org (2010-07-01)

filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=41487. Working on the fix.

### pk...@chromium.org (2010-07-01)

Please CC me on that WK bug so I can see it.  Please also tell me what additional problems you think you see, as they may not be problems or the fixes may be subtle.

### in...@chromium.org (2010-07-01)

Peter, here are some other ones i see problematic, please let me know if they need to be corrected too.

trunk/src/third_party/WebKit/WebCore/platform/image-decoders/gif/GIFImageDecoder.cpp - Matches: 2
   331:   // This is the first frame, so we're not relying on any previous data.
   332:   if (!buffer->setSize(scaledSize().width(), scaledSize().height()))
   333:       return setFailed();
   361:   // image, results in a completely empty image.
   362:   if (!buffer->setSize(bufferSize.width(), bufferSize.height()))
   363:       return setFailed();

trunk/src/third_party/WebKit/WebCore/platform/image-decoders/bmp/BMPImageReader.cpp - Matches: 2
    80:   if (m_buffer->status() == RGBA32Buffer::FrameEmpty) {
    81:       if (!m_buffer->setSize(m_parent->size().width(), m_parent->size().height()))
    82:           return m_parent->setFailed(); // Unable to allocate.

### pk...@chromium.org (2010-07-01)

No, those are all fine.  You're confusing RGBA32Buffer::setSize() with ImageDecoder::setSize().  The two are in unrelated class hierarchies.

### pk...@chromium.org (2010-07-01)

In fact, to be clearer, if you were to remove the "setFailed()" calls in those cases, you would break things badly :)

### in...@chromium.org (2010-07-01)

thanks peter for confirming. i will fix the jpeg decoder one.

### in...@chromium.org (2010-07-02)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-07-02)

Fixed in r62399: <http://trac.webkit.org/changeset/62399>. Marking as Fixed since it never touched stable.

### sc...@gmail.com (2010-07-08)

Thanks for catching this regression before it got anywhere near the Stable channel, Aki! This qualifies for a $500 reward :)

### ao...@gmail.com (2010-07-09)

Great :) This one goes to Red Cross.

### sc...@gmail.com (2010-07-12)

Done! $1337 to Red Cross, thanks.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/48115?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081931)*
