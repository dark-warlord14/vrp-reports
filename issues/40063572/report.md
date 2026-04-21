# LAN9500, LAN75xx driver information leak

| Field | Value |
|-------|-------|
| **Issue ID** | [40063572](https://issues.chromium.org/issues/40063572) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Core |
| **Platforms** | ChromeOS |
| **Reporter** | sz...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2023-03-13 |
| **Bounty** | $1,000.00 |

## Description

---

### Report description


LAN9500, LAN75xx driver information leak


---

### Bug location


#### Which product or website have you found a vulnerability in?

Other - Chrome VRP


#### Which URL (or repository) have you found the vulnerability in?

Chrome OS - Linux Kernel


---

### The problem


#### Please describe the technical details of the vulnerability

*Summary*

Drivers for LAN9500 and LAN75xx USB ethernet adapters may be exploited to disclose contents of kernel memory.

*Description*

The drivers for LAN9500 and LAN75xx USB ethernet adapters include an issue in handling of packet length extracted from the retrieved data chunk.

Looking at the implementation of rx_fixup procedures in both kernel modules (smsc95xx_rx_fixup, smsc75xx_rx_fixup) one may notice that validation does not assure that the packet length is smaller than the skb->len, which initially represents the actual USB transfer length (as assigned in usbnet). The packet length extracted from received payload and susceptible to malicious modification is assigned as the packet length of a cloned socket buffer (ax_skb) which in turn is passed to the network stack (usbnet_skb_return).

Consequently, this issue may be exploited to leak contents of kernel memory to the network stack and a unprivileged user (e.g. malicious device sends crafted UDP with checksum set to 0x00 which will be delivered to a listening UDP server executed by an unprivileged user).

Furthermore, with specific setup contents of kernel memory may be leaked via response messages returned to the malicious device. For example when ICMP "port not available" messages are enabled sending a crafted UDP message to a port without any listening application will result in sending back the mentioned ICMP message including UDP request payload which for a malicious message in turn will include contents of the kernel memory. It's also possible to utilize ICMP echo requests yet this requires brute forcing or guessing the checksum calculated over part of provided malicious message along with kernel memory contents. Yet due to the variation of memory contents this approach has slightly reduced success rate.

For the LAN9500 driver packet size may be up to 1526 bytes, for LAN75xx the value increases up to 9026 bytes due to support for jumbo frames.

drivers/net/usb/smsc75xx.c
```
	while (skb->len > 0) {
		u32 rx_cmd_a, rx_cmd_b, align_count, size;
		struct sk_buff *ax_skb;
		unsigned char *packet;

		rx_cmd_a = get_unaligned_le32(skb->data);
		skb_pull(skb, 4);

		rx_cmd_b = get_unaligned_le32(skb->data);
		skb_pull(skb, 4 + RXW_PADDING);

		packet = skb->data;

		/* get the packet length */
		size = (rx_cmd_a & RX_CMD_A_LEN) - RXW_PADDING;
		align_count = (4 - ((size + RXW_PADDING) % 4)) % 4;
```

```
			ax_skb = skb_clone(skb, GFP_ATOMIC);
			if (unlikely(!ax_skb)) {
				netdev_warn(dev->net, "Error allocating skb\n");
				return 0;
			}

			ax_skb->len = size;
			ax_skb->data = packet;
			skb_set_tail_pointer(ax_skb, size);

			smsc75xx_rx_csum_offload(dev, ax_skb, rx_cmd_a,
				rx_cmd_b);

			skb_trim(ax_skb, ax_skb->len - 4); /* remove fcs */
			ax_skb->truesize = size + sizeof(struct sk_buff);

			usbnet_skb_return(dev, ax_skb);
```

drivers/net/usb/smsc95xx.c
```
		header = get_unaligned_le32(skb->data);
		skb_pull(skb, 4 + NET_IP_ALIGN);
		packet = skb->data;

		/* get the packet length */
		size = (u16)((header & RX_STS_FL_) >> 16);
		align_count = (4 - ((size + NET_IP_ALIGN) % 4)) % 4;
```

```
			ax_skb = skb_clone(skb, GFP_ATOMIC);
			if (unlikely(!ax_skb)) {
				netdev_warn(dev->net, "Error allocating skb\n");
				return 0;
			}

			ax_skb->len = size;
			ax_skb->data = packet;
			skb_set_tail_pointer(ax_skb, size);

			if (dev->net->features & NETIF_F_RXCSUM)
				smsc95xx_rx_csum_offload(ax_skb);
			skb_trim(ax_skb, ax_skb->len - 4); /* remove fcs */
			ax_skb->truesize = size + sizeof(struct sk_buff);

			usbnet_skb_return(dev, ax_skb);
```


Kernel configuration entries for LAN9500 and LAN75xx drivers - CONFIG_USB_NET_SMSC95XX and CONFIG_USB_NET_SMSC75XX accordingly - are enabled as modules in all current kernel branches for ChromeOS. This issue dates back to the original implementation from Kernel 2.6 (commits 2f7ca802bdae2ca41022618391c70c2876d92190 and d0cad871703b898a442e4049c532ec39168e5b57) so all past versions of Chrome OS supporting mentioned drivers are affected.

Please find attached sample patches addressing the issues for both mentioned kernel modules.

*Impact*

Potentially sensitive information from kernel memory space may be leaked.

*Reproduction steps*

- connect the malicious USB device to host
- enumerate as LAN9500 or LAN75xx to bind vulnerable kernel module
- send an IN USB bulk transfer crafted to have packet size larger than skb->len
- observe that the crafted packet results in creation of a cloned skb with length larger than the original skb->len
- observe that the socket buffer data will include portions of extra kernel memory contents
- observe that contents of kernel memory may be accessed by a unprivileged local user (e.g. via UDP)
- observe that in certain configurations, i.e. with enabled ICMP port not available kernel memory contents may be extracted over the USB network interface

*Expected mitigation*

Prevent manipulation of skb->len by improving validation of packet length extracted from received data payload.

*Affected version*

All




#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

Unpriviledged user may exploit the issue to retrieve contents of kernel memory, potentially including sensitive information.


---

### The cause


#### What version of Chrome have you found the security issue in?

All


#### Is the security issue related to a crash?

No


#### Choose the type of vulnerability

Sensitive data exposure


#### How would you like to be publicly acknowledged for your report?

SZYMON HEIDRICH




## Attachments

- [0001-net-usb-smsc75xx-Limit-packet-length-to-skb-len.patch](attachments/0001-net-usb-smsc75xx-Limit-packet-length-to-skb-len.patch) (text/plain, 1.3 KB)
- [0001-net-usb-smsc95xx-Limit-packet-length-to-skb-len.patch](attachments/0001-net-usb-smsc95xx-Limit-packet-length-to-skb-len.patch) (text/plain, 1.2 KB)

## Timeline

### sz...@gmail.com (2023-03-13)

[Empty comment from Monorail migration]

### ch...@appspot.gserviceaccount.com (2023-03-13)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-03-13)

[Empty comment from Monorail migration]

### en...@google.com (2023-03-14)

Thank you for the report.
Assigning to roxabee@ while we decide on an official course of action for upstream kernel bug reports.

### sz...@gmail.com (2023-03-15)

Hello,

Please find upstream patches under following links:
- https://patchwork.kernel.org/project/linux-usb/patch/20230313220045.52394-1-szymon.heidrich@gmail.com/
- https://patchwork.kernel.org/project/linux-usb/patch/20230313220124.52437-1-szymon.heidrich@gmail.com/


### sz...@gmail.com (2023-03-18)

Hello,

FYI changes addressing the mentioned issue for LAN9500 and LAN75xx were merged to netdev:
- https://git.kernel.org/pub/scm/linux/kernel/git/netdev/net.git/commit/?id=ff821092cf02a70c2bccd2d19269f01e29aa52cf
- https://git.kernel.org/pub/scm/linux/kernel/git/netdev/net.git/commit/?id=d8b228318935044dafe3a5bc07ee71a1f1424b8d
- https://git.kernel.org/pub/scm/linux/kernel/git/netdev/net.git/commit/?id=43ffe6caccc7a1bb9d7442fbab521efbf6c1378c


### [Deleted User] (2023-03-19)

[Empty comment from Monorail migration]

### ch...@google.com (2023-03-21)

Your report will be worked on in the Buganizer system but we will still provide progress updates here as well! 


### ch...@google.com (2023-03-21)

[Empty comment from Monorail migration]

[Monorail blocking: b/274563379]

### sz...@gmail.com (2023-03-21)

Thank you for the information, please let me know in case you would need additional input from my side.

### ro...@google.com (2023-03-28)

Thank you for reporting this bug to upstream so they can release a fix. However I am struggling to see a credible attack scenario where this bug could actually be exploited on ChromeOS. An attack would require a malicious usb connected to the host as well as a malicious program running in user space. ChromeOS does not allow running arbitrary user space programs. 

Do you have any ideas on how this bug can be exploited and constitutes a vulnerability in ChromeOS?

### ro...@google.com (2023-03-28)

[Empty comment from Monorail migration]

### ro...@google.com (2023-03-28)

[Empty comment from Monorail migration]

### sz...@gmail.com (2023-03-28)

Possibly I'm not up to date but some vectors would be:
- Linux on ChromeOS
- chrome.sockets.udp API for Extansions/Apps
- ICMP echo requests with bruteforced/guessed checksum

Other protocols I didn't consider could also likely be useful for exploitation.



### [Deleted User] (2023-03-28)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-04-12)

Marking as fixed because of following comment at buganizer:

Marked as fixed.
Upstream commit ff821092cf0 ("net: usb: smsc95xx: Limit packet length to skb->len")
  Integrated in v6.3-rc4
  Fixed in chromeos-6.1 with merge of v6.1.22 (sha e041bef1adee)
    Not in R102, R108, R110, R111, R112
  Fixed in chromeos-5.15 with merge of v5.15.105 (sha ba6c40227108)
    Not in R102, R108, R110, R111, R112
  Fixed in chromeos-5.10 with merge of v5.10.177 (sha 33d1603a38e0)
    Not in R102, R108, R110, R111, R112
  Fixed in chromeos-5.4 with merge of v5.4.240 (sha f2111c791d88)
    Not in R102, R108, R110, R111, R112
  Fixed in chromeos-4.19 with merge of v4.19.280 (sha d3c145a4d24b)
    Not in R102, R108, R110, R111, R112
  Fixed in chromeos-4.14 with merge of v4.14.312 (sha 733580e268a5)
    Not in R102, R108, R110, R111, R112

### [Deleted User] (2023-04-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-12)

[Empty comment from Monorail migration]

### pa...@chromium.org (2023-04-25)

Thank you for the high quality report and the patches!

I agree with Low severity given the preconditions for successful attack.

Setting FoundIn-75 because that's as far back as we go with that tag, I think.

[Monorail components: Internals>Core]

### am...@google.com (2023-04-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-28)

Congratulations, Szymon! The VRP Panel has decided to award you $1,000 for this information leak bug + $2,000 patch bonus given that you authored the patch as well as committed the patch upstream. Thank you for your efforts and reporting this issue to us. 

### sz...@gmail.com (2023-04-28)

Hello Amy, thank you very much for the great news and wish you a splendid weekend.

### am...@google.com (2023-04-29)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-07-19)

This issue was migrated from crbug.com/chromium/1424177?no_tracker_redirect=1

[Monorail blocking: b/274563379]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063572)*
