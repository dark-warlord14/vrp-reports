# UAF in EnclaveWebSocketClient::OnConnectionEstablished

| Field | Value |
|-------|-------|
| **Issue ID** | [370133761](https://issues.chromium.org/issues/370133761) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebAuthentication |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | jt...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2024-09-29 |
| **Bounty** | $6,000.00 |

## Description

**VULNERABILITY DETAILS**

In WebAuthn, the Enclave Authenticator uses WebSockets to communicate with server. Every time when performing a transaction with the enclave, a websocket connection would be initialized. In function `EnclaveWebSocketClient::OnConnectionEstablished`, if there is pending data to send, it calls `InternalWrite` and then resets `pending_write_data_` [1]. However, `InternalWrite` may call to `ClosePipe` and delete itself [2], which results in UAF when accessing the member variable `pending_write_data_`.

This is because `EnclaveWebSocketClient::OnConnectionEstablished` calls `WebSockets.StartReceiving` before sending data through the writable data pipe [3]. The mojo call `StartReceiving` tells the Network Service to read more frame from the remote side, and if the connection has been closed (e.g. due to network error or server response), it will drop the channel and reset all data pipe [4]. In this case, EnclaveWebSocketClient will fail to send message and destroy itself.

```
void EnclaveWebSocketClient::OnConnectionEstablished(...) {
  websocket_->StartReceiving();      // ===> [3]

  state_ = State::kOpen;

  if (pending_write_data_) {
    InternalWrite(*pending_write_data_);
    pending_write_data_ = std::nullopt;      // ===> [1] UAF here
  }
}

void EnclaveWebSocketClient::InternalWrite(base::span<const uint8_t> data) {
  CHECK(state_ == State::kOpen);

  websocket_->SendMessage(network::mojom::WebSocketMessageType::BINARY,
                          data.size());
  MojoResult result = writable_->WriteAllData(data);
  if (result != MOJO_RESULT_OK) {
    FIDO_LOG(ERROR) << "Failed to write to WebSocket.";
    ClosePipe(SocketStatus::kError);      // ===> [2] delete this
  }
}

void WebSocket::WebSocketEventHandler::OnDropChannel(
    bool was_clean,
    uint16_t code,
    const std::string& reason) {
  impl_->client_->OnDropChannel(was_clean, code, reason);
  impl_->Reset();      // ===> [4]
}

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:device/fido/enclave/enclave_websocket_client.cc;l=208;drc=9ffdf5bc515eeb4e7f308a74477f0b28cc96f029>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:device/fido/enclave/enclave_websocket_client.cc;l=156;drc=f522344e45882da4c7f7cb1b3a0a7bd747d654bb>

[3] <https://source.chromium.org/chromium/chromium/src/+/main:device/fido/enclave/enclave_websocket_client.cc;l=202;drc=9ffdf5bc515eeb4e7f308a74477f0b28cc96f029>

[4] <https://source.chromium.org/chromium/chromium/src/+/main:services/network/websocket.cc;l=317;drc=f522344e45882da4c7f7cb1b3a0a7bd747d654bb>

**VERSION**

Chrome Version: beta + dev

**REPRODUCTION CASE**

It requires a signed-in user calls `navigator.credentials` related JS API to trigger this, however signing in to custom build Chromium is normally restricted and I don't find a way to fake a signed-in user without a large code patch. So I reuse the browser test code for a easy reproduction in local asan environment.

Tested on Chromium version 131.0.6735.0, Linux platform

1. Apply the attached patch.diff
2. Run
   ninja -C out/Asan browser\_tests
   out/Asan/browser\_tests --gtest\_filter=EnclaveAuthenticatorWithPinBrowserTest.RegisterDeviceWithGpmPin\_MakeCredential\_Success

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Type of crash: browser
Crash State: see asan.log for details

**Bisection**

This was introduced in <https://chromium.googlesource.com/chromium/src/+/9934f322060c9808cff85f64af8448c4f608826f>

**Fix Suggestion**

Use a stack-alloc variable to hold value of `pending_write_data_` and clear `pending_write_data_` before calling InternalWrite.

```
diff --git a/device/fido/enclave/enclave_websocket_client.cc b/device/fido/enclave/enclave_websocket_client.cc
index b3d42475d53ee..4bb2d9c5cc05c 100644
--- a/device/fido/enclave/enclave_websocket_client.cc
+++ b/device/fido/enclave/enclave_websocket_client.cc
@@ -204,8 +204,8 @@ void EnclaveWebSocketClient::OnConnectionEstablished(
   state_ = State::kOpen;
 
   if (pending_write_data_) {
-    InternalWrite(*pending_write_data_);
-    pending_write_data_ = std::nullopt;
+    auto pending_write_data = std::exchange(pending_write_data_, std::nullopt).value();
+    InternalWrite(pending_write_data);
   }
 }

```

## Attachments

- [patch.diff](attachments/patch.diff) (text/x-diff, 1.4 KB)
- [asan.log](attachments/asan.log) (text/plain, 29.2 KB)

## Timeline

### th...@chromium.org (2024-09-30)

Hi reporter, it would be helpful if you can attach a POC that can be loaded in Chrome (or at least an ASAN stack trace from running a POC on Chrome). That helps me assess the severity of the bug. Could you please add that? Please also note any command line arguments that are needed.

For now, setting FoundIn to 128 based on the bisect CL, but note that I have not reproduced this. Adding kenrb@ to cc also based on bisect CL, but not yet assigning since this issue is not yet fully triaged.

### ke...@chromium.org (2024-09-30)

Thanks for the report. This is valid.

It is a browser-process UAF but would be difficult for web content to deliberately trigger, because it requires causing a specific failure in a WebSocket write that the page doesn't control. It might be useful as part of a chain, though.

The preconditions warrant Medium severity, I'd say.

### pe...@google.com (2024-09-30)

Setting milestone because of s2 severity.

### ap...@google.com (2024-09-30)

Project: chromium/src  

Branch: main  

Author: Ken Buchanan <[kenrb@chromium.org](mailto:kenrb@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5900439>

[WebAuthn] Clear pending write socket data state before sending it

---


Expand for full commit details
```
[WebAuthn] Clear pending write socket data state before sending it

`EnclaveWebSocketClient` should not modify member variables after
calling `InternalWrite`.

Fixed: 370133761
Change-Id: Id29639790583d15bfa82e261ffcd40867a006dd0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5900439
Reviewed-by: Adam Langley <agl@chromium.org>
Commit-Queue: Ken Buchanan <kenrb@chromium.org>
Auto-Submit: Ken Buchanan <kenrb@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1362071}

```

---

Files:

- M `device/fido/enclave/enclave_websocket_client.cc`
- M `device/fido/enclave/enclave_websocket_client.h`

---

Hash: d59a0f272fb3a889a5dd3fd669f6958078153dbe  

Date:  Mon Sep 30 22:51:18 2024


---

### pe...@google.com (2024-10-01)

Security Merge Request Consideration: Requesting merge to beta (M130) because latest trunk commit (1362071) appears to be after beta branch point (1356013).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pe...@google.com (2024-10-01)

The NextAction date has arrived: 2024-10-01
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### pe...@google.com (2024-10-01)

Merge review required: M130 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), gmpritchard (ChromeOS), danielyip (Desktop)

### am...@chromium.org (2024-10-02)

<https://crrev.com/c/5900439> approved for merge to M130; please merge this fix to branch 6723 at your earliest convenience so this fix can be included in the next M130 beta update (and by EOD Monday 7 October, so this fix can be included in the forthcoming M130 Stable RC cut)

### ap...@google.com (2024-10-02)

Project: chromium/src  

Branch: refs/branch-heads/6723  

Author: Ken Buchanan <[kenrb@chromium.org](mailto:kenrb@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5904659>

[WebAuthn] Clear pending write socket data state before sending it

---


Expand for full commit details
```
[WebAuthn] Clear pending write socket data state before sending it

`EnclaveWebSocketClient` should not modify member variables after
calling `InternalWrite`.

(cherry picked from commit d59a0f272fb3a889a5dd3fd669f6958078153dbe)

Fixed: 370133761
Change-Id: Id29639790583d15bfa82e261ffcd40867a006dd0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5900439
Reviewed-by: Adam Langley <agl@chromium.org>
Commit-Queue: Ken Buchanan <kenrb@chromium.org>
Auto-Submit: Ken Buchanan <kenrb@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1362071}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5904659
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/6723@{#845}
Cr-Branched-From: 985f2961df230630f9cbd75bd6fe463009855a11-refs/heads/main@{#1356013}

```

---

Files:

- M `device/fido/enclave/enclave_websocket_client.cc`
- M `device/fido/enclave/enclave_websocket_client.h`

---

Hash: 53e18fa5cbf5ed9280fe375e76ac91ba772fd331  

Date:  Wed Oct 02 20:11:32 2024


---

### sp...@google.com (2024-10-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $6000.00 for this report.

Rationale for this decision:
$4,000 for report of moderately mitigated memory corruption in a non-sandboxed process + $1,000 bisect bonus + $1,000 patch bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-10-03)

Congratulations Rong! Due to the extent of the preconditions to exploit this issue, as summarized in c#3, we considered this to be somewhat heavily mitigated. However, due to the high quality of the report, but mostly demonstrating the impacts in security-sensitive code, we have considered it as moderately mitigated and subject to a slightly higher reward. Thank you for your efforts and reporting this issue to us -- great work!

### pe...@google.com (2025-01-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/370133761)*
