# Security: UAF in TransportClientSocket

| Field | Value |
|-------|-------|
| **Issue ID** | [40060984](https://issues.chromium.org/issues/40060984) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Network |
| **Platforms** | Android, Windows |
| **Reporter** | le...@gmail.com |
| **Assignee** | li...@chromium.org |
| **Created** | 2022-09-15 |
| **Bounty** | $11,000.00 |

## Description

**VULNERABILITY DETAILS**  

If the network sandbox is enabled on Win or Android, it will use `BrokeredClientSocketFactory`[1] to create a `TCPClientSocketBrokered`[2] as `transport_socket_`[3] to handle the `TransportConnect`[4].

```
std::unique_ptr<net::TransportClientSocket>  
BrokeredClientSocketFactory::CreateTransportClientSocket(  
    const net::AddressList& addresses,  
    std::unique_ptr<net::SocketPerformanceWatcher> socket_performance_watcher,  
    net::NetworkQualityEstimator\* network_quality_estimator,  
    net::NetLog\* net_log,  
    const net::NetLogSource& source) {  
  if (ShouldBroker(addresses)) {  
    return std::make_unique<TCPClientSocketBrokered>(       <<<---------- [2]  
        addresses, std::move(socket_performance_watcher),  
        network_quality_estimator, net_log, source, this);  
  }  
  
  return std::make_unique<net::TCPClientSocket>(  
      addresses, std::move(socket_performance_watcher),  
      network_quality_estimator, net_log, source);  
}  
  
int TransportConnectSubJob::DoEndpointLockComplete() {  
  [...]  
   transport_socket_ =                                      <<<---------- [3]  
      parent_job_->client_socket_factory()->CreateTransportClientSocket(  
          one_address, std::move(socket_performance_watcher),  
          parent_job_->network_quality_estimator(), net_log.net_log(),  
          net_log.source());  
  [...]  
  return transport_socket_->Connect(base::BindOnce(         <<<---------- [5]  
      &TransportConnectSubJob::OnIOComplete, base::Unretained(this)));  
}  
  

```

The `transport_socket_` will bind[5] a callback function `OnIOComplete` as parameter to call `Connect`. The function `Connect` will finally call `DidCompleteConnect` to run[6] the callback.

```
void TCPClientSocketBrokered::DidCompleteConnect(  
    net::CompletionOnceCallback callback,  
    int result) {  
  DCHECK_NE(result, net::ERR_IO_PENDING);  
  
  std::move(callback).Run(result);                         <<<---------- [6]  
  is_connect_in_progress_ = false;                         <<<---------- [8]  
}  

```

However, the callback function `OnIOComplete` will call `DoTransportConnectComplete`[7] to handle the connect result. And if `result != OK`, the `transport_socket_` will be reset. Thus, when it back to the TCPClientSocketBrokered scope, accessing[8] its member variables will trigger this uaf.

```
void TransportConnectSubJob::OnIOComplete(int result) {  
  int rv = DoLoop(result);  
  if (rv != ERR_IO_PENDING)  
    parent_job_->OnSubJobComplete(rv, this);  // |this| deleted  
}  
  
int TransportConnectSubJob::DoLoop(int result) {  
  [...]  
	case STATE_TRANSPORT_CONNECT_COMPLETE:  
        rv = DoTransportConnectComplete(rv);               <<<---------- [7]  
        break;  
  [...]  
}  
  
int TransportConnectSubJob::DoTransportConnectComplete(int result) {  
  next_state_ = STATE_DONE;  
  if (result != OK) {  
    // Drop the socket to release the endpoint lock, if any.  
    transport_socket_.reset();  
    [...]  
  }  
}  

```

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:services/network/network_context.cc;l=2614;drc=4f446f9b4760f7f62ea05a946cfeeafea4fb5d6d>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/main:services/network/brokered_client_socket_factory.cc;l=54;drc=c96b91805f93a1dc515de0be6c0f628ae24570c1>  

[3]. <https://source.chromium.org/chromium/chromium/src/+/main:net/socket/transport_connect_sub_job.cc;l=219;drc=6459548ee396bbe1104978b01e19fcb1bb68d0e5>  

[4]. <https://source.chromium.org/chromium/chromium/src/+/main:net/socket/transport_connect_sub_job.cc;l=181;drc=6459548ee396bbe1104978b01e19fcb1bb68d0e5>

[5]. <https://source.chromium.org/chromium/chromium/src/+/main:net/socket/transport_connect_sub_job.cc;l=246;drc=6459548ee396bbe1104978b01e19fcb1bb68d0e5>  

[6]. <https://source.chromium.org/chromium/chromium/src/+/main:services/network/tcp_client_socket_brokered.cc;l=102;drc=e20990e149669a5554b29e8eca4044515679a36e>

[7]. <https://source.chromium.org/chromium/chromium/src/+/main:net/socket/transport_connect_sub_job.cc;l=184;drc=6459548ee396bbe1104978b01e19fcb1bb68d0e5>  

[8]. <https://source.chromium.org/chromium/chromium/src/+/main:services/network/tcp_client_socket_brokered.cc;l=103;drc=e20990e149669a5554b29e8eca4044515679a36e>

**VERSION**

Win & Android.

Head with NetworkServiceSandbox.

Bisect:  

<https://source.chromium.org/chromium/chromium/src/+/c96b91805f93a1dc515de0be6c0f628ae24570c1>

**REPRODUCTION CASE**

$ python3 -m http.server 8000  

$ out/asan/chrome.exe --user-data-dir=xxxx --enable-features=NetworkServiceSandbox "<http://localhost:8000/poc.html>" --no-sandbox

(use no-sandbox to log network process asan trace)

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: network process  

Crash State: see asan file.

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Vulnerability Research Institute

## Attachments

- [asan](attachments/asan) (text/plain, 16.1 KB)
- [poc.html](attachments/poc.html) (text/plain, 58 B)

## Timeline

### [Deleted User] (2022-09-15)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-09-15)

davidben, looks like you've been active in this file recently. Could you please take a look or re-assign as appropriate?

Found-in set 107 per reporter's bisect. Please doublecheck.

[Monorail components: Internals>Network]

### da...@chromium.org (2022-09-15)

Traveling this week, but reassigning to liza for the socket brokering stuff.

### [Deleted User] (2022-09-15)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-09-15)

I think the fix is to just swap the order of the callback and the is_connect_in_progress_ line. We generally have to assume that callbacks in //net can destroy the object, and either do that last, or play goofy WeakPtr games when that's not possible.

### li...@chromium.org (2022-09-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/36583d670be1a7da30e9812d5a5d1276a22e6430

commit 36583d670be1a7da30e9812d5a5d1276a22e6430
Author: Liza Burakova <liza@chromium.org>
Date: Thu Sep 15 21:51:11 2022

Fix UAF in TCPClientSocketBrokered

Bug: 1363998
Change-Id: Id909505651ff1815983f341a549bec6aee69d837
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3899416
Reviewed-by: Matt Menke <mmenke@chromium.org>
Commit-Queue: Liza Burakova <liza@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1047698}

[modify] https://crrev.com/36583d670be1a7da30e9812d5a5d1276a22e6430/services/network/tcp_client_socket_brokered.cc


### [Deleted User] (2022-09-16)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-16)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### li...@chromium.org (2022-09-19)

Changing security_impact to none as the network service sandbox is not enabled in Android or Windows atm.

### [Deleted User] (2022-09-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-19)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-30)

Congratulations, Leecraso and Guang Gong! The VRP Panel has decided to award you $10,000 for this report + $1,000 bisect bonus. Thank you for your efforts in reporting this issue to us -- great work! 

### am...@google.com (2022-10-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2022-11-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1363998?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060984)*
