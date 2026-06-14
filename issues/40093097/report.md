#  redefine unconfiguable length attribute of array object

| Field | Value |
|-------|-------|
| **Issue ID** | [40093097](https://issues.chromium.org/issues/40093097) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | hi...@gmail.com |
| **Assignee** | ya...@chromium.org |
| **Created** | 2018-11-17 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36

Steps to reproduce the problem:
this is a issue related with https://bugs.chromium.org/p/chromium/issues/detail?id=905940
we know, the length attribute of array in v8 is an unconfigurable accessinfo and should not be redefined, but the following function can change the length attribute to configuable and the the length attribute can be deleted and redefined.

MaybeHandle<JSArray> ValueDeserializer::ReadSparseJSArray() {
  // If we are at the end of the stack, abort. This function may recurse.
  STACK_CHECK(isolate_, MaybeHandle<JSArray>());

  uint32_t length;
  if (!ReadVarint<uint32_t>().To(&length)) return MaybeHandle<JSArray>();

  uint32_t id = next_id_++;
  HandleScope scope(isolate_);
  Handle<JSArray> array = isolate_->factory()->NewJSArray(
      0, TERMINAL_FAST_ELEMENTS_KIND, pretenure_);
  JSArray::SetLength(array, length);
  AddObjectWithID(id, array);

  uint32_t num_properties;
  uint32_t expected_num_properties;
  uint32_t expected_length;
  if (!ReadJSObjectProperties(array, SerializationTag::kEndSparseJSArray, false)    ------------->this function can redefine length attribute
           .To(&num_properties) ||
      !ReadVarint<uint32_t>().To(&expected_num_properties) ||
      !ReadVarint<uint32_t>().To(&expected_length) ||
      num_properties != expected_num_properties || length != expected_length) {
    return MaybeHandle<JSArray>();
  }

  DCHECK(HasObjectWithID(id));
  return scope.CloseAndEscape(array);

Maybe<uint32_t> ValueDeserializer::ReadJSObjectProperties(
    Handle<JSObject> object, SerializationTag end_tag,
    bool can_use_transitions) {
  uint32_t num_properties = 0;

  // Fast path (following map transitions).
  if (can_use_transitions) {
    bool transitioning = true;
    Handle<Map> map(object->map(), isolate_);
    DCHECK(!map->is_dictionary_map());
    DCHECK_EQ(0, map->instance_descriptors()->number_of_descriptors());
    std::vector<Handle<Object>> properties;
    properties.reserve(8);

    while (transitioning) {
      // If there are no more properties, finish.
      SerializationTag tag;
      if (!PeekTag().To(&tag)) return Nothing<uint32_t>();
      if (tag == end_tag) {
        ConsumeTag(end_tag);
        CommitProperties(object, map, properties);
        CHECK_LT(properties.size(), std::numeric_limits<uint32_t>::max());
        return Just(static_cast<uint32_t>(properties.size()));
      }

      // Determine the key to be used and the target map to transition to, if
      // possible. Transitioning may abort if the key is not a string, or if no
      // transition was found.
      Handle<Object> key;
      Handle<Map> target;
      TransitionsAccessor transitions(isolate_, map);
      Handle<String> expected_key = transitions.ExpectedTransitionKey();
      if (!expected_key.is_null() && ReadExpectedString(expected_key)) {
        key = expected_key;
        target = transitions.ExpectedTransitionTarget();
      } else {
        if (!ReadObject().ToHandle(&key) || !IsValidObjectKey(key)) {
          return Nothing<uint32_t>();
        }
        if (key->IsString()) {
          key =
              isolate_->factory()->InternalizeString(Handle<String>::cast(key));
          // Don't reuse |transitions| because it could be stale.
          transitioning = TransitionsAccessor(isolate_, map)
                              .FindTransitionToField(Handle<String>::cast(key))
                              .ToHandle(&target);
        } else {
          transitioning = false;
        }
      }

      // Read the value that corresponds to it.
      Handle<Object> value;
      if (!ReadObject().ToHandle(&value)) return Nothing<uint32_t>();

      // If still transitioning and the value fits the field representation
      // (though generalization may be required), store the property value so
      // that we can copy them all at once. Otherwise, stop transitioning.
      if (transitioning) {
        int descriptor = static_cast<int>(properties.size());
        PropertyDetails details =
            target->instance_descriptors()->GetDetails(descriptor);
        Representation expected_representation = details.representation();
        if (value->FitsRepresentation(expected_representation)) {
          if (expected_representation.IsHeapObject() &&
              !target->instance_descriptors()
                   ->GetFieldType(descriptor)
                   ->NowContains(value)) {
            Handle<FieldType> value_type =
                value->OptimalType(isolate_, expected_representation);
            Map::GeneralizeField(isolate_, target, descriptor,
                                 details.constness(), expected_representation,
                                 value_type);
          }
          DCHECK(target->instance_descriptors()
                     ->GetFieldType(descriptor)
                     ->NowContains(value));
          properties.push_back(value);
          map = target;
          continue;
        } else {
          transitioning = false;
        }
      }

      // Fell out of transitioning fast path. Commit the properties gathered so
      // far, and then start setting properties slowly instead.
      DCHECK(!transitioning);
      CHECK_LT(properties.size(), std::numeric_limits<uint32_t>::max());
      CommitProperties(object, map, properties);
      num_properties = static_cast<uint32_t>(properties.size());

      bool success;
      LookupIterator it = LookupIterator::PropertyOrElement(
          isolate_, object, key, &success, LookupIterator::OWN);
      if (!success ||
          JSObject::DefineOwnPropertyIgnoreAttributes(&it, value, NONE)       -------------->DefineOwnPropertyIgnoreAttributes can define the length attribute to configuable 
              .is_null()) {
        return Nothing<uint32_t>();
      }
      num_properties++;
    }

    // At this point, transitioning should be done, but at least one property
    // should have been written (in the zero-property case, there is an early
    // return).
    DCHECK(!transitioning);
    DCHECK_GE(num_properties, 1u);
  }

  // Slow path.
  for (;; num_properties++) {
    SerializationTag tag;
    if (!PeekTag().To(&tag)) return Nothing<uint32_t>();
    if (tag == end_tag) {
      ConsumeTag(end_tag);
      return Just(num_properties);
    }

    Handle<Object> key;
    if (!ReadObject().ToHandle(&key) || !IsValidObjectKey(key)) {
      return Nothing<uint32_t>();
    }
    Handle<Object> value;
    if (!ReadObject().ToHandle(&value)) return Nothing<uint32_t>();

    bool success;
    LookupIterator it = LookupIterator::PropertyOrElement(
        isolate_, object, key, &success, LookupIterator::OWN);
    if (!success ||
        JSObject::DefineOwnPropertyIgnoreAttributes(&it, value, NONE)
            .is_null()) {
      return Nothing<uint32_t>();
    }
  }
}

}

As length attribute is important to an array, redine the length is dangerous, it should be easy to exploit it.

What is the expected behavior?

What went wrong?
the length attribute should not be redefined

Did this work before? N/A 

Chrome version: 70.0.3538.102  Channel: stable
OS Version: 10.0
Flash Version:

## Timeline

### hi...@gmail.com (2018-11-19)

[Comment Deleted]

### ve...@chromium.org (2018-11-19)

[Empty comment from Monorail migration]

### ya...@chromium.org (2018-11-19)

Thanks for the bug report. I'll take a look at this.

### ha...@chromium.org (2018-11-19)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### dr...@chromium.org (2018-11-19)

Assigning high severity because it sounds like it could lead to memory corruption in the renderer process. Feel free to lower if it turns out to be hard to exploit.

### bu...@chromium.org (2018-11-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/2603bb051e9b31802419a47bff03bb8ec7bb0641

commit 2603bb051e9b31802419a47bff03bb8ec7bb0641
Author: Yang Guo <yangguo@chromium.org>
Date: Tue Nov 20 10:59:36 2018

Only expect new data properties in ValueDeserializer.

Bug: chromium:906313
Change-Id: Ie5d91e086d02433e2dec7728e29e4ae87cdd34c3
Reviewed-on: https://chromium-review.googlesource.com/c/1340290
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Commit-Queue: Yang Guo <yangguo@chromium.org>
Cr-Commit-Position: refs/heads/master@{#57632}
[modify] https://crrev.com/2603bb051e9b31802419a47bff03bb8ec7bb0641/src/value-serializer.cc
[modify] https://crrev.com/2603bb051e9b31802419a47bff03bb8ec7bb0641/test/unittests/value-serializer-unittest.cc


### ya...@chromium.org (2018-11-20)

Not sure whether we should also merge this to M70?

### sh...@chromium.org (2018-11-20)

This bug requires manual review: We are only 13 days from stable.
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-11-20)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-11-20)

hablich@ & awhalley@ for M71 merge review. Cl listed at #6 is not yet baked in canary.

### sh...@chromium.org (2018-11-20)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@chromium.org (2018-11-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-11-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/af004818616aecb442ae4269609493c4791721d9

commit af004818616aecb442ae4269609493c4791721d9
Author: Yang Guo <yangguo@chromium.org>
Date: Wed Nov 21 12:05:55 2018

Merged: Only expect new data properties in ValueDeserializer.

Revision: 2603bb051e9b31802419a47bff03bb8ec7bb0641

TBR=hablich@chromium.org
BUG=chromium:906313
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true

Change-Id: I5b3c951748b68f5ab8552348302d0842dd5f061c
Reviewed-on: https://chromium-review.googlesource.com/c/1346118
Reviewed-by: Yang Guo <yangguo@chromium.org>
Cr-Commit-Position: refs/branch-heads/7.1@{#48}
Cr-Branched-From: f70aaa8ab2e8815505a6145c745e50d8328cd28c-refs/heads/7.1.302@{#1}
Cr-Branched-From: 1dbcc78efa17a9047f7e923958087ef9eec43066-refs/heads/master@{#56462}
[modify] https://crrev.com/af004818616aecb442ae4269609493c4791721d9/src/value-serializer.cc
[modify] https://crrev.com/af004818616aecb442ae4269609493c4791721d9/test/unittests/value-serializer-unittest.cc


### go...@chromium.org (2018-11-21)

This is already merged at #13. Removing "Merge-Approved-71" label.

### sh...@chromium.org (2018-11-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-12-03)

Nice one higongguang@! The VRP panel decided to award $3,000 for this report - cheers!

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/906313?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093097)*
