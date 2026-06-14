# Security: Insecure behavior in /tmp by Keystone on Mac OS X

| Field | Value |
|-------|-------|
| **Issue ID** | [40081127](https://issues.chromium.org/issues/40081127) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Reporter** | go...@vtty.com |
| **Assignee** | mo...@google.com |
| **Created** | 2010-05-20 |
| **Bounty** | $500.00 |

## Description

Basics:  Insecure /tmp file handling by keystone may allow privilege escalation or removal of files.  

Project: update-engine

Looking at KSDownloadAction.m, it launches ksurlPath:

>> NSString *ksurlPath = [self ksurlPath];
>> ...
>>   [downloadTask_ setLaunchPath:ksurlPath];
>> ...
>> [downloadTask_ launch];

ksurlPath is generated writing out the binary in a generated path, then returning that path by doing:
>>  NSString *directory = [self ksurlValidatedDirectory];
>> NSString *destination = [directory stringByAppendingPathComponent:@"ksurl"];
>> NSNumber *properPermission = [NSNumber numberWithUnsignedLong:0755];
>>  if ([[NSFileManager defaultManager] createFileAtPath:destination contents:ksdata attributes:attr] == NO) {

ksurlValidatedDirectory either creates what it thinks is a safe directory, or returns nil and a failure is caught.  It creates the directory like this:
>> NSString *directory = [self ksurlDirectoryName];

  -- Here, ksrulDirectoryName returns the following:
  >> NSString *directory = [NSString stringWithFormat:@"/tmp/.ksda.%X", geteuid()];
  This is an easily guessable filename.  Anyone can expect it will be created.  Also note that every reboot, and periodically, files in /tmp/ are cleared, 
which means that this path will be wiped away a lot, even if it already exists.  Keep this in mind as we continue.

>> if ([self isValidAndSafeDirectory:directory]) {return directory;}

  -- isValidAndSafeDirectory is then used to determine if the directory is owned by the right person.  However there are flaws in this logic.  This 
method only checks the permissions and ownership, but not the device.  This path could have been created in a filesystem mounted in /tmp.  Any 
user could do this, meaning that Keystone may trust a path controlled by another user.  From this point the user has control over where this file will 
be written.

>> [[NSFileManager defaultManager] removeFileAtPath:directory handler:nil];

  -- if for some reason this check fails, such as a potential attacker, the code then attempts to recursively remove files at this path.  However, the 
starting point of the removal is not validated.  This may lead to removal of files at path controlled by an attacker.

Another take on the attack:
1.  Attacker mounts remote filesystem in /tmp/.ksda.1F5 with root node having "appropriate" ownership and permissions (501/0755)
2.  Attacker waits for keystone updater to run
3.  Attacker controls remote filesystem, and makes sure when ksda runs, the binary is replaced with a different binary

I have seen a screenshot from a user indicating that least in some versions, the updater is run as root.  I have not been able to reproduce that, but it 
seems as though this could be used to execute commands as the user who keystone updater is executed as.

Solution:  Ksda should use a securely created temporary directory, not rely on some easily guessable path, which is not properly checked, and 
insecurely handled.



## Timeline

### go...@vtty.com (2010-05-20)

This was based off of a very quick scan of the code, and I did not have the time to build a proof of concept.  I 
thought it would be better to be safe than sorry, and have you guys take a peek to verify if I am correct that this 
is exploitable, or not.

### js...@chromium.org (2010-05-20)

mark@ - can you take a look at this and either grab it or assist in finding an owner?

### ma...@chromium.org (2010-05-20)

Filed http://b/2701124.

### go...@vtty.com (2010-05-20)

I verified that this runs as root - Chrome just installed itself in my system when enabling Chrome updates

### js...@chromium.org (2010-05-25)

Tracking here until the buganizer report is closed out.

### ma...@chromium.org (2010-06-01)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-06-04)

googlecode@vtty.com - Thanks for the report. We're working on a fix for this 
issue and will inform you when all affected products are patched and a disclosure can 
be made.


### js...@chromium.org (2010-06-04)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-06-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-06-29)

Updates are rolling out to Chrome, but we have to keep this unreleased until other products update.


### in...@chromium.org (2010-07-14)

[Empty comment from Monorail migration]

### go...@vtty.com (2010-07-15)

Thanks!

### in...@chromium.org (2010-07-15)

[Empty comment from Monorail migration]

### go...@vtty.com (2010-08-09)

Curious if there is an update on this...

### js...@chromium.org (2010-08-09)

Sorry for the delay in responding. The keystone update was pushed out in June to all deployed installations. However, the updater is embedded in the installation package for several products, and a few of these packages have not yet been updated. This means that a new installation may use a vulnerable keystone package for a brief window until it is automatically updated (generally within 24hrs). We expect the last remaining products to be updated in a few weeks, and plan delaying release of this vulnerability until then.


### sc...@gmail.com (2010-08-13)

@googlecode@vtty.com - congrats! We'd like to provisionally offer you a $500 Chromium Security Award for reporting this bug to us. Thanks for your continued discretion whilst the fix works its way into all the non-Chrome installers.

### sc...@gmail.com (2010-09-29)

Payment is in electronic system.

### js...@chromium.org (2010-10-29)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### go...@vtty.com (2011-04-27)

Is this fixed everywhere yet?


### ma...@chromium.org (2011-04-27)

As far as I’m aware, it’s fixed in most places, but there may still be some products that bundle an old version. Those users would be affected if it was their initial Keystone installation until Keystone upgraded itself.

### go...@vtty.com (2011-04-27)

Thanks for the quick update -- I was just wondering if it was okay to talk publicly about it yet.

### js...@chromium.org (2011-04-27)

Given that you reported this over a year ago, I don't think we can reasonably ask you to delay disclosure.

### ma...@chromium.org (2011-04-27)

Well, almost a year ago, but I agree.

### js...@chromium.org (2011-04-27)

Basic arithmetic has never been my strong suit.

### js...@chromium.org (2011-10-05)

Batch update: Final fuzzy classification of security bugs affecting stable.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/44658?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081127)*
