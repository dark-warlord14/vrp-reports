# Security: The serialized data is corrupted because the return value is always true.

| Field | Value |
|-------|-------|
| **Issue ID** | [40093435](https://issues.chromium.org/issues/40093435) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hi...@gmail.com |
| **Assignee** | jb...@chromium.org |
| **Created** | 2018-12-13 |
| **Bounty** | $1,000.00 |

## Description

The serialized data is corrupted because the return value is always true.

Look at the call stack about serializing an ImageData object using V8ScriptValueSerializer
https://cs.chromium.org/chromium/src/third_party/blink/renderer/bindings/core/v8/serialization/v8_script_value_serializer.cc?rcl=7fa1000f175eeb5e0ee75287ab8c69feb13fdd2d&l=202
bool V8ScriptValueSerializer::WriteDOMObject(ScriptWrappable* wrappable,
                                             ExceptionState& exception_state) {
  const WrapperTypeInfo* wrapper_type_info = wrappable->GetWrapperTypeInfo();
  ......
  if (wrapper_type_info == V8ImageData::GetWrapperTypeInfo()) {
    ImageData* image_data = wrappable->ToImpl<ImageData>();
    WriteTag(kImageDataTag);
    SerializedColorParams color_params(image_data->GetCanvasColorParams(),
                                       image_data->GetImageDataStorageFormat());
    WriteUint32Enum(ImageSerializationTag::kCanvasColorSpaceTag);
    WriteUint32Enum(color_params.GetSerializedColorSpace());
    WriteUint32Enum(ImageSerializationTag::kImageDataStorageFormatTag);
    WriteUint32Enum(color_params.GetSerializedImageDataStorageFormat());
    WriteUint32Enum(ImageSerializationTag::kEndTag);
    WriteUint32(image_data->width());
    WriteUint32(image_data->height());
    DOMArrayBufferBase* pixel_buffer = image_data->BufferBase();
    uint32_t pixel_buffer_length =
        SafeCast<uint32_t>(pixel_buffer->ByteLength());
    WriteUint32(pixel_buffer_length);
    WriteRawBytes(pixel_buffer->Data(), pixel_buffer_length);  ==========> this write may fail, of cause, the above WriteUint32,WriteUint32Enum may be fail too.
    return true;              ===================> but this function always return true.
  }
 ......
}

see the code about aforementioned WriteRawBytes
https://cs.chromium.org/chromium/src/third_party/blink/renderer/bindings/core/v8/serialization/v8_script_value_serializer.h?rcl=7fa1000f175eeb5e0ee75287ab8c69feb13fdd2d&l=58
  void WriteRawBytes(const void* data, size_t size) {
    serializer_.WriteRawBytes(data, size);
  }

https://cs.chromium.org/chromium/src/v8/src/api.cc?rcl=146487a6764cd9ef5bd623eb828e9754fb09a5ba&l=3121
void ValueSerializer::WriteRawBytes(const void* source, size_t length) {
  private_->serializer.WriteRawBytes(source, length);
}

eventually, it will call ValueSerializer::WriteRawBytes
https://cs.chromium.org/chromium/src/v8/src/value-serializer.cc?rcl=146487a6764cd9ef5bd623eb828e9754fb09a5ba&l=278
void ValueSerializer::WriteRawBytes(const void* source, size_t length) {
  uint8_t* dest;
  if (ReserveRawBytes(length).To(&dest)) {   ==========> ReserveRawBytes may fail due to no memory and no data will be written into buffer but V8ScriptValueSerializer::WriteDOMObject still return true.
    memcpy(dest, source, length);
  }
}


So, serialize the following arr2 can generate corrupted data, 

block = Alloc(0x7fffffff);===>first we allocate many memory, almost exhaust all memory the render can allocate. 

var arr2 = [];
function call_back() {

	block.terminate();  //this call will free all memory in worker thread "block";
	sleep(2000);
	return [1, 2, 3, 4, 5, 6, 7, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1];
}

arr2[0] = new ImageData(0x1ffff, 0x1000);==========>serializing this object will fail because of the function ReserveRawBytes fail due to no memory, but because the return value is wrong, serialization will continue.
arr2.__defineGetter__(1, call_back);     ==========>when serialize the second element, many memory will be freed by the call_back function.
arr2[2] = new ImageData(0x1ffff, 0x1000);==========>so serializing this object will succeed, but the serialized data is already corrupted because the data of the first ImageData object is lost.


there are many other wrapper_type_info in the function V8ScriptValueSerializer::WriteDOMObject is wrongly return true when being serialized.
  if (wrapper_type_info == V8DOMPointReadOnly::GetWrapperTypeInfo()) {
    DOMPointReadOnly* point = wrappable->ToImpl<DOMPointReadOnly>();
    WriteTag(kDOMPointReadOnlyTag);
    WriteDouble(point->x());
    WriteDouble(point->y());
    WriteDouble(point->z());
    WriteDouble(point->w()); ==================> WriteDouble may  fail too,
    return true;      ==================> always return true
  }
  if (wrapper_type_info == V8DOMRect::GetWrapperTypeInfo()) {
    DOMRect* rect = wrappable->ToImpl<DOMRect>();
    WriteTag(kDOMRectTag);
    WriteDouble(rect->x());
    WriteDouble(rect->y());
    WriteDouble(rect->width());
    WriteDouble(rect->height());
    return true;    ==================> always return true
  }
  if (wrapper_type_info == V8DOMRectReadOnly::GetWrapperTypeInfo()) {
    DOMRectReadOnly* rect = wrappable->ToImpl<DOMRectReadOnly>();
    WriteTag(kDOMRectReadOnlyTag);
    WriteDouble(rect->x());
    WriteDouble(rect->y());
    WriteDouble(rect->width());
    WriteDouble(rect->height());
    return true;    ==================> always return true
  }
  if (wrapper_type_info == V8DOMQuad::GetWrapperTypeInfo()) {
    DOMQuad* quad = wrappable->ToImpl<DOMQuad>();
    WriteTag(kDOMQuadTag);
    for (const DOMPoint* point :
         {quad->p1(), quad->p2(), quad->p3(), quad->p4()}) {
      WriteDouble(point->x());
      WriteDouble(point->y());
      WriteDouble(point->z());
      WriteDouble(point->w());
    }
    return true;     ==================> always return true
  }
  if (wrapper_type_info == V8DOMMatrix::GetWrapperTypeInfo()) {
    DOMMatrix* matrix = wrappable->ToImpl<DOMMatrix>();
    if (matrix->is2D()) {
      WriteTag(kDOMMatrix2DTag);
      WriteDouble(matrix->a());
      WriteDouble(matrix->b());
      WriteDouble(matrix->c());
      WriteDouble(matrix->d());
      WriteDouble(matrix->e());
      WriteDouble(matrix->f());
    } else {
      WriteTag(kDOMMatrixTag);
      WriteDouble(matrix->m11());
      WriteDouble(matrix->m12());
      WriteDouble(matrix->m13());
      WriteDouble(matrix->m14());
      WriteDouble(matrix->m21());
      WriteDouble(matrix->m22());
      WriteDouble(matrix->m23());
      WriteDouble(matrix->m24());
      WriteDouble(matrix->m31());
      WriteDouble(matrix->m32());
      WriteDouble(matrix->m33());
      WriteDouble(matrix->m34());
      WriteDouble(matrix->m41());
      WriteDouble(matrix->m42());
      WriteDouble(matrix->m43());
      WriteDouble(matrix->m44());
    }
    return true;    ==================> always return true
  }


there are some other functions which is always return true such as 
bool V8ScriptValueSerializer::WriteFile
bool V8ScriptValueSerializer::WriteFile(File* file,
                                        ExceptionState& exception_state) {
  serialized_script_value_->BlobDataHandles().Set(file->Uuid(),
                                                  file->GetBlobDataHandle());
  if (blob_info_array_) {
    size_t index = blob_info_array_->size();
    DCHECK_LE(index, std::numeric_limits<uint32_t>::max());
    long long size = -1;
    double last_modified_ms = InvalidFileTime();
    file->CaptureSnapshot(size, last_modified_ms);
    // FIXME: transition WebBlobInfo.lastModified to be milliseconds-based also.
    double last_modified = last_modified_ms / kMsPerSecond;
    blob_info_array_->emplace_back(file->GetBlobDataHandle(), file->GetPath(),
                                   file->name(), file->type(), last_modified,
                                   size);
    WriteUint32(static_cast<uint32_t>(index));
  } else {
    WriteUTF8String(file->HasBackingFile() ? file->GetPath() : g_empty_string);
    WriteUTF8String(file->name());
    WriteUTF8String(file->webkitRelativePath());
    WriteUTF8String(file->Uuid());
    WriteUTF8String(file->type());
    // TODO(jsbell): metadata is unconditionally captured in the index case.
    // Why this inconsistency?
    if (file->HasValidSnapshotMetadata()) {
      WriteUint32(1);
      long long size;
      double last_modified_ms;
      file->CaptureSnapshot(size, last_modified_ms);
      DCHECK_GE(size, 0);
      WriteUint64(static_cast<uint64_t>(size));
      WriteDouble(last_modified_ms);
    } else {
      WriteUint32(0);
    }
    WriteUint32(file->GetUserVisibility() == File::kIsUserVisible ? 1 : 0);
  }
  return true;==========> always return true, but the above write operation may fail too
}


## Timeline

### hi...@gmail.com (2018-12-13)

this is an issue related with https://bugs.chromium.org/p/chromium/issues/detail?id=905940

### ca...@chromium.org (2018-12-13)

jbroman: Passing on to you since you own the other bug.

[Monorail components: Blink>JavaScript]

### jb...@chromium.org (2018-12-13)

Hmm. I think we can handle all of these upstream by checking v8::internal::ValueSerializer::out_of_memory_ after calling WriteHostObject, and failing there. That seems likely to be less error-prone than having to expose the expansion state in the V8 API, though we may eventually have to do that.

The out_of_memory_ flag would still fail on the next value, but apparently we reset that flag on every entry to v8::i::ValueSerializer::WriteObject, even recursive ones. :(

Thanks for the explanation; that makes perfect sense.

### jb...@chromium.org (2018-12-13)

binji@, you added the OOM logic to ValueSerializer in https://chromium.googlesource.com/v8/v8.git/+/966355585bb3e6e21c063c2b670045f5a75e5aa5; do you remember why out_of_memory_ is reset to false in WriteObject?

Not having it wouldn't be the cleanest thing here, but it seems like it would have mitigated this attack to now be able to return from an exhausted-memory state. (In fact I could even see replacing it with "if we've already failed to realloc the buffer once, give up eagerly in WriteObject".)

### bi...@chromium.org (2018-12-13)

jbroman@, hard to remember but I'd guess it was just an oversight. Sorry about that.

### jb...@chromium.org (2018-12-14)

[Empty comment from Monorail migration]

### jb...@chromium.org (2018-12-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-12-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/8494c583ca1daf1208d272db038c1cee727548a8

commit 8494c583ca1daf1208d272db038c1cee727548a8
Author: Jeremy Roman <jbroman@chromium.org>
Date: Fri Dec 14 16:41:52 2018

ValueSerializer: Report if buffer expansion fails during WriteHostObject.

Also fail early if we detect that we've previously run out of memory and thus
corrupted the buffer.

Add a unit test for this kind of case.

Bug: chromium:914731
Change-Id: Iaaf3927209bffeab6fe8ba462d9dd9dad8cbbe2f
Reviewed-on: https://chromium-review.googlesource.com/c/1377449
Reviewed-by: Yang Guo <yangguo@chromium.org>
Commit-Queue: Jeremy Roman <jbroman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#58248}
[modify] https://crrev.com/8494c583ca1daf1208d272db038c1cee727548a8/src/value-serializer.cc
[modify] https://crrev.com/8494c583ca1daf1208d272db038c1cee727548a8/test/unittests/value-serializer-unittest.cc


### sh...@chromium.org (2018-12-29)

jbroman: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jb...@chromium.org (2019-01-03)

Fix appears to prevent this path from being reachable; checked on Linux and Win x64.

### sh...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-06)

This bug requires manual review: M72 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), djmm@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-01-07)

+awhalley@ (Security TPM) for M72 merge review.

### aw...@google.com (2019-01-07)

govind@ - good for M72

### go...@chromium.org (2019-01-07)

Approving merge to M72 branch 3626 based on https://crbug.com/chromium/914731#c15. Please merge ASAP so we can pick it up for this week beta release, RC cut tomorrow noon. Thank you.

### go...@chromium.org (2019-01-07)

Pls merge your change to M72 branch 3626 ASAP (latest by 12:00 PM PT, tomorrow, 12/08) so we can pick it up for this week beta release on Wednesday. Thank you.

### na...@google.com (2019-01-07)

[Empty comment from Monorail migration]

### jb...@chromium.org (2019-01-08)

[Empty comment from Monorail migration]

### bu...@chromium.org (2019-01-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/dd9eae86d8a5dfbc761c5d9e25d04a9ca4edcfea

commit dd9eae86d8a5dfbc761c5d9e25d04a9ca4edcfea
Author: Jeremy Roman <jbroman@chromium.org>
Date: Tue Jan 08 19:25:26 2019

Merged: ValueSerializer: Report if buffer expansion fails during WriteHostObject.

Revision: 8494c583ca1daf1208d272db038c1cee727548a8

BUG=chromium:914731
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=yangguo@chromium.org

Change-Id: I77a81edec553b5affd83f434418ea8530ff0d9ef
Reviewed-on: https://chromium-review.googlesource.com/c/1398684
Reviewed-by: Yang Guo <yangguo@chromium.org>
Reviewed-by: Adam Klein <adamk@chromium.org>
Commit-Queue: Adam Klein <adamk@chromium.org>
Cr-Commit-Position: refs/branch-heads/7.2@{#37}
Cr-Branched-From: 6acd03c9b8a8232aee95f25fbf6ae822aaedae75-refs/heads/7.2.502@{#1}
Cr-Branched-From: b03041de094610ef24e0e4fb6bf4c700fa1553ed-refs/heads/master@{#57910}
[modify] https://crrev.com/dd9eae86d8a5dfbc761c5d9e25d04a9ca4edcfea/src/value-serializer.cc
[modify] https://crrev.com/dd9eae86d8a5dfbc761c5d9e25d04a9ca4edcfea/test/unittests/value-serializer-unittest.cc


### jb...@chromium.org (2019-01-08)

Merged:
https://chromium-review.googlesource.com/c/v8/v8/+/1398684
https://chromium.googlesource.com/v8/v8/+/dd9eae86d8a5dfbc761c5d9e25d04a9ca4edcfea

### na...@google.com (2019-01-09)

jbroman - What is the impact of this report?

### jb...@chromium.org (2019-01-10)

The bug allows invalid data to be processed by the message deserializer, which exposes its attack surface. (It's not intended that an attacker be able to throw arbitrary data at the deserializer without first compromising a renderer or similar.) 

The issue originally reported as https://crbug.com/chromium/905940 used this bug to inject corrupt data into the deserializer, and then exploited another bug (fixed in 905940) to write out of bounds.

So this bug isn't itself massive per se, but fixing it would have made exploiting 905940 more difficult.

### na...@google.com (2019-01-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### pa...@chromium.org (2019-01-17)

Congrats! The Panel decided to reward $1,000 for this report :) 

### aw...@google.com (2019-01-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2019-05-13)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-05-17)

[Empty comment from Monorail migration]

### is...@google.com (2019-05-17)

This issue was migrated from crbug.com/chromium/914731?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093435)*
