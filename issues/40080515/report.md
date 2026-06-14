# Chrome exploit: V8 properties + P2PHostMsg_Send

| Field | Value |
|-------|-------|
| **Issue ID** | [40080515](https://issues.chromium.org/issues/40080515) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Unknown |
| **Reporter** | ae...@chromium.org |
| **Assignee** | ya...@chromium.org |
| **Created** | 2014-09-22 |
| **Bounty** | $27,634.00 |

## Description

See writeup.pdf.

1. V8 slow / fast properties confusion

Code in src/objects.cc:4089:
MaybeHandle<Object> JSObject::SetOwnPropertyIgnoreAttributes(
  ..
  object­>LookupOwn(name, &lookup, true);
  ..
  if (is_observed && lookup.IsProperty()) { 
    if (lookup.IsDataProperty()) { 
      old_value = Object::GetPropertyOrElement(object, name).ToHandleChecked(); 
    } 
    old_attributes = lookup.GetAttributes(); 
  } 
  ..
  switch (lookup.type()) { 
    case NORMAL: 
      ReplaceSlowProperty(object, name, value, attributes);

GetPropertyOrElement() can invoke a getter. The getter can transform object to fast properties, confusing ReplaceSlowProperty() into corrupting memory. The lookup.IsDataProperty() actually checks whether name is a getter. And it takes some trickery to get past that. See writeup.pdf.

This bug was fixed by refactoring on August 18, but still impacts current stable and beta. I got the renderer arbitrary R/W to work on Android and 64-bit linux. I think it should work on Windows as well.


2. P2PHostMsg_Send OOB write

content/browser/renderer_host/p2p/socket_dispatcher_host.cc:269:
void P2PSocketDispatcherHost::OnSend(int socket_id,
                                     ...
                                     const rtc::PacketOptions& options,

content/browser/renderer_host/p2p/socket_host.cc:131:
void UpdateRtpAuthTag(char* rtp, int len,
                      const rtc::PacketOptions& options) {
  ...
  size_t tag_length = options.packet_time_params.srtp_auth_tag_len;
  char* auth_tag = rtp + (len ­ tag_length);
  ...
  if (hmac.DigestLength() < tag_length) {
    NOTREACHED();
    return;
  }
  ...
  memcpy(auth_tag, &options.packet_time_params.srtp_packet_index, 4);
  ...
  memcpy(auth_tag, output, tag_length);

The srtp_auth_tag_len field is renderer-controlled and lacks validation. The first memcpy OOB writes 4 bytes if srtp_auth_tag_len == 0. socket_host.cc also has a bunch of other issues. See writeup.pdf.


Chrome Version:
  37.0.2062.120 stable
  38.0.2125.66 beta

Operating System:
  Renderer R/W: all
  Sandbox break: 64-bit linux

Reproduction:
- run ./webserver inside v8p2p/
- navigate to http://localhost:8000/v8p2p/v8p2p.html
- /etc/passwd is displayed


## Attachments

- [writeup.pdf](attachments/writeup.pdf) (application/pdf, 157.0 KB)
- [v8p2p.tar.gz](attachments/v8p2p.tar.gz) (application/x-gzip, 180.2 KB)

## Timeline

### ve...@chromium.org (2014-09-22)

Arg. Thanks for the report. Adding rafaelw@ who owns the O.o code. Adding adamk@ since rafaelw@ may still be OOO.

I'd be inclined to turn off O.o again until this is fixed (or my refactoring hits stable). I'll leave it up to adamk@ / rafaelw@ though.

### ve...@chromium.org (2014-09-22)

+rossberg@: FYI

### ve...@chromium.org (2014-09-22)

Ok, just assigning it to rafaelw@ was a bit premature; my apologies. There's obviously other stuff to be done. I'll pick up at least the JSON part of this.

### ve...@chromium.org (2014-09-22)

Fixed the JSON parsing part in https://codereview.chromium.org/592813002/

### da...@chromium.org (2014-09-22)

[Empty comment from Monorail migration]

### wf...@chromium.org (2014-09-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-09-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-09-22)

Jww@, this will be the master tracking bug. Please file additional sub-bugs (blocked on this) after triaging.

### cl...@chromium.org (2014-09-22)

[Empty comment from Monorail migration]

### pa...@chromium.org (2014-09-22)

And thanks again, Jüri! :) Great work as always.

### in...@chromium.org (2014-09-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-09-22)

[Empty comment from Monorail migration]

### ae...@chromium.org (2014-09-22)

Hey Chris, thanks :)

If you guys would cc me on sub-bugs, that would be great.

### wf...@chromium.org (2014-09-22)

impact -> none, severity -> critical, as this is the parent bug.  See child bugs - https://crbug.com/chromium/416526 and https://crbug.com/chromium/416528.

### in...@chromium.org (2014-09-22)

Thanks Juri, cced you on both.

### cl...@chromium.org (2014-09-22)

[Empty comment from Monorail migration]

### ad...@chromium.org (2014-09-22)

I'm probably a better Object.observe contact for this than Rafael. Can someone please CC me on the the sub-bugs?

Turning off O.o should be considered a last resort, given that it's been on by default for more than an entire release.

### jw...@chromium.org (2014-09-22)

adamk@, I CC'd you on the observe sub-bug.

### cl...@chromium.org (2014-09-23)

[Empty comment from Monorail migration]

### ve...@chromium.org (2014-09-24)

I don't think anything needs to be done on the O.o side. It was just a simple step along the way to provoke the bug.

The JSON part (entry-point) is fixed, and Yang backmerged a CHECK (which will crash) in SetNormalizedProperty, the backend function that was used to corrupt the heap.

Reassigning to yangguo@ since I'm unexpectedly OOO.

### ya...@chromium.org (2014-09-24)

This has been merged back to M37 and M38 with additional CHECK to prevent slow/fast mode confusion when setting a property. Marking this as fixed.

### am...@google.com (2014-09-24)

Is there a merge required here?

### ya...@chromium.org (2014-09-24)

The fix has been merged to older V8 branches:
V8 3.28.71.12 (r24162) for M38
V8 3.27.34.21 (r24125) for M37
I guess the DEPS file will need to be updated to pick up the changes in Chromium.

### cl...@chromium.org (2014-09-24)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-09-24)

Thanks!

### in...@chromium.org (2014-09-24)

Actually this is the meta bug, fixing labels in https://crbug.com/chromium/416526.

### mb...@chromium.org (2014-10-06)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-10-07)

Hey Jüri - the reward for this bug is $27.633.70! It's comprised of:

$15,000 for the sandbox escape + exploit
$7,500 for the renderer RCE + exploit
+$2,000 for the patch ($1,000 for the first one, plus an additional $1,000 for picking up the bug in the original patch)
+$3,133.7 for your linux l33tness IPC memory corruption on 64-bit linux!

Congratulations!

### ti...@chromium.org (2014-10-07)

[Empty comment from Monorail migration]

### ae...@chromium.org (2014-10-07)

Thank you!

### ti...@google.com (2014-12-08)

Payment in progress

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-31)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-01-01)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

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

### st...@gmail.com (2018-10-03)

https://crbug.com/chromium/416449


### jo...@chromium.org (2018-10-03)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-03)

This issue was migrated from crbug.com/chromium/416449?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/416526, crbug.com/chromium/416528]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080515)*
