# Security: Chrome OS : Two security bugs of mwifiex

| Field | Value |
|-------|-------|
| **Issue ID** | [40066948](https://issues.chromium.org/issues/40066948) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | pi...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-07-06 |
| **Bounty** | $1,500.00 |

## Description

**VULNERABILITY DETAILS**

Hi Team,

While reviewing marvell wifi driver mwifiex used by chromebooks, I found 2 security bugs. I have send them to [security@kernel.org](mailto:security@kernel.org) and linux kernel maillists, [security@kernel.org](mailto:security@kernel.org) let me wait for maillists' responses.

<https://crbug.com/chromium/1>:

<https://lore.kernel.org/linux-wireless/20230706020751.859773-1-pinkperfect2021@gmail.com/>

Userspace program with CAP\_NET\_ADMIN in its namespace can send netlink messages to config wifi driver, which is called cfg80211 flow. Use unshare(CLONE\_NEWUSER) + unshare(CLONE\_NEWNET) can get CAP\_NET\_ADMIN in the new namespace, this is the tech used by many network modules exploits.

When handling netlink messages, mwifiex\_set\_encode doesn't check key\_len and seq\_len, which can cause controllable memory overwriting.  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v6.1/drivers/net/wireless/marvell/mwifiex/sta_ioctl.c;drc=828c91f7937f62b0c60c86af63772c4161962e6a;l=1096>

```
    if (key_len)  
        memcpy(encrypt_key.key_material, key, key_len);  <---------  
    else  
        encrypt_key.is_current_wep_key = true;  

    if (mac_addr)  
        memcpy(encrypt_key.mac_addr, mac_addr, ETH_ALEN);  
    if (kp && kp->seq && kp->seq_len) {  
        memcpy(encrypt_key.pn, kp->seq, kp->seq_len); <-----------  
        encrypt_key.pn_len = kp->seq_len;  
        encrypt_key.is_rx_seq_valid = true;  
    }  

```

These checks should be done in cfg80211 function cfg80211\_validate\_key\_settings, but mwifiex has a unusual cipher mode WLAN\_CIPHER\_SUITE\_SMS4 in mwifiex\_cipher\_suites, if the input cipher mode is WLAN\_CIPHER\_SUITE\_SMS4, cfg80211\_validate\_key\_settings will not check the key\_len and seq\_len, wifi driver itself is responsible for checking them.

<https://crbug.com/chromium/2>:

<https://lore.kernel.org/linux-wireless/20230705044350.838428-1-pinkperfect2021@gmail.com/>

This bug is in the call path of handling packets from wifi firmware, mwifiex\_process\_mgmt\_packet  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v6.1/drivers/net/wireless/marvell/mwifiex/util.c;drc=828c91f7937f62b0c60c86af63772c4161962e6a;l=378>

In outside functions have checked the upper limit of rx\_pkt\_length, in mwifiex\_process\_mgmt\_packet should also make sure not underflow.

```
rx_pd = (struct rxpd \*)skb->data;  

skb_pull(skb, le16_to_cpu(rx_pd->rx_pkt_offset));  
skb_pull(skb, sizeof(pkt_len));  

pkt_len = le16_to_cpu(rx_pd->rx_pkt_length);  

ieee_hdr = (void \*)skb->data;  
if (ieee80211_is_mgmt(ieee_hdr->frame_control)) {  
    if (mwifiex_parse_mgmt_packet(priv, (u8 \*)ieee_hdr,  
                      pkt_len, rx_pd))  
        return -1;  
}  
/\* Remove address4 \*/  
memmove(skb->data + sizeof(struct ieee80211_hdr_3addr),  
    skb->data + sizeof(struct ieee80211_hdr),  
    pkt_len - sizeof(struct ieee80211_hdr));  <---------------- if pkt_len < sizeof(struct ieee80211_hdr), memmove can cause oob write  

```

**CREDIT INFORMATION**

Reporter credit: [lovepink]

## Timeline

### [Deleted User] (2023-07-06)

[Empty comment from Monorail migration]

### pm...@chromium.org (2023-07-06)

[Empty comment from Monorail migration]

### ch...@google.com (2023-07-06)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/290187254). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/290187254]

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### ch...@google.com (2023-08-01)

Project: chromiumos/third_party/kernel
Branch: chromeos-5.10

commit ec4489ef763dbe402e0fdad766ffecf764acd754
Author: Polaris Pi <pinkperfect2021@gmail.com>
Date:   Sun Jul 23 07:07:41 2023

    FROMLIST: wifi: mwifiex: Fix OOB and integer underflow when rx packets
   
    Make sure mwifiex_process_mgmt_packet,
    mwifiex_process_sta_rx_packet and mwifiex_process_uap_rx_packet,
    mwifiex_uap_queue_bridged_pkt and mwifiex_process_rx_packet
    not out-of-bounds access the skb->data buffer.
   
    Fixes: 2dbaf751b1de ("mwifiex: report received management frames to cfg80211")
    Signed-off-by: Polaris Pi <pinkperfect2021@gmail.com>
    (am from https://patchwork.kernel.org/patch/13323091/)
    (also found at https://lore.kernel.org/r/20230723070741.1544662-1-pinkperfect2021@gmail.com)
   
    BUG=b:290187254
    TEST=wifi_matfunc on kevin
    UPSTREAM-TASK=b:291980011
   
    Change-Id: Ibbb2d79599742f56d5e1a59dc65cd642a5f712b0
    Signed-off-by: Matthew Wang <matthewmwang@chromium.org>
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4703165
    Reviewed-by: Sean Paul <sean@poorly.run>
    Reviewed-by: Abhishek Kumar <kuabhs@chromium.org>

M       drivers/net/wireless/marvell/mwifiex/sta_rx.c
M       drivers/net/wireless/marvell/mwifiex/uap_txrx.c
M       drivers/net/wireless/marvell/mwifiex/util.c

https://chromium-review.googlesource.com/4703165

### [Deleted User] (2023-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-01)

[Empty comment from Monorail migration]

### pi...@gmail.com (2023-08-16)

For reward panel: You can check https://crbug.com/chromium/2 details and PoC in https://crbug.com/chromium/290187254 comments: #6 #8 #9 #52

### jo...@chromium.org (2023-08-22)

[Empty comment from Monorail migration]

### ch...@google.com (2023-09-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-13)

This bug is a regression and does not impact stable or extended stable.Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-09-18)

Exploitability
This kernel bug is exploitable by compromised WiFi firmware. As per https://crbug.com/chromium/1462551#c55, this is a WiFi firmware to kernel escalation, which bypasses a protection domain. It requires the user to have previously compromised the WiFi firmware. While this cannot be done remotely, attacking WiFi firmware doesn't require physical presence, as with directional antennas WiFi range can be extended to the hundreds of meters.

Privileges and Capabilities
As per https://crbug.com/chromium/1462551#c55, this bug allows an attacker with code execution in the WiFi firmware to overwrite memory in the kernel.

Origin of fix
The fix was provided by the reporter.

Mitigations
This issue is mitigated by the fact that the attacker needs code execution in the WiFi firmware. Code execution in WiFi firmware is not uncommon, but it's still a mitigation.

Severity assessment
Bypassing a protection domain (peripheral to kernel) is high severity, P1. We could consider this mitigated down to a medium because of the requirement of WiFi firmware code exec.

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-05)

Congratulations lovepink! 
The VRP Panel has decided to award you $1500 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions.

### ch...@google.com (2023-10-05)

[Empty comment from Monorail migration]

### am...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-11-07)

This issue was migrated from crbug.com/chromium/1462551?no_tracker_redirect=1

[Monorail blocking: b/290187254]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40066948)*
