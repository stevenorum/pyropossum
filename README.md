# pyropossum

pyropossum is a collection of tools for home automation, currently focused on making it easy to remotely control stuff.  In the future, it may also be expanded to include sensors and data reading.

## Setup
The following terms are used to differentiate the different pieces of the system:

Receiver host: A computer with accessible digital I/O pins that is waiting to receive instructions by listening on an AWS SQS queue.  (For reference, I'm using a Raspberry Pi Zero Wireless, as it's more than powerful enough and costs $10.)

Sender host: A computer that sends instructions to the AWS SQS queue.  (For reference, I'm just using my laptop.)

### How to set up the pyropossum AWS stack and the sender host:
(All steps/links will assume the region is us-east-1, but this can be used in pretty much any AWS region.  us-east-1 just happens to be the geographically closest to me.)
1. Go to [the CloudFormation console](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks "CloudFormation Console (us-east-1)") and create a CloudFormation stack using the [pyropossum.cf.json](cloudformation/pyropossum.cf.json) template.
2. Go to [the IAM console](https://console.aws.amazon.com/iam/home?region=us-east-1#/users "IAM Console").  There will be two users, <SystemID>SenderUser and <SystemID>ReceiverUser.  For each one, click on the username, then click on the "Security credentials" tab, then click on the "Create access key" button.  Click "show" to see the secret key, and then copy both the access and secret key to a text file.  Make sure to keep track of which pair is for the SenderUser and which pair is for the ReceiverUser.
3. Put the SenderUser creds into the file ~/.aws/credentials on the sender host, in the following format:
```
[pyropossum-send]
aws_access_key_id=AKIAXXXXXXXXXXXXXXXX
aws_secret_access_key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```
4. Put the following information into the file ~/.pyropossum/config.json ([here's my config as an example](config/send-config.json)):
```
{
    "send-profile":"<the name in brackets in the credentials file>",
    "region":"<AWS region name>",
    "stack":"<CloudFormation stack name>"
}
```

5. Install pyropossum from the command line.  The following line will do it, but you really should make sure to examine the [install script](install/sender-install.sh) first before piping it directly to sudo bash.
```
curl https://raw.githubusercontent.com/stevenorum/pyropossum/master/install/sender-install.sh | sudo bash
```
6. At this point, you should be ready to signal your stack.  You can do that with the following two commands:
```
pyro-on
pyro-off
```
(The commands won't do anything until your receiver-host is set up, obviously.)

### How to set up the receiver host for use with pyropossum:
1. If you're using a Raspberry Pi, you can use [PiBakery](http://www.pibakery.org) and [the included recipe](pibakery-recipe.xml) to perform a lot of the setup.  (You'll need to edit it to include your passwords, wifi info, and that sort of thing.)

2. If you don't want to use PiBakery, you can instead install this from the [receiver-install.sh](install/receiver-install.sh) script.  It has dependencies on python3 and pip3.  Everything after that it should install for you.

3. Connect the relays for your devices to digital output pins and update the pin map in pyro-daemon to have your mapping.

4. In order to make sure the relays trigger, I'm using the output pins as base controllers for a transistor, which acts a switch to connect or disconnect the relay to the 5V output.  Normal RPi pins are only designed to output between 3mA (if all are in use) and 16mA (if only one is in use) (source for this is some random forum post; I can't verify that it's 100% correct).  In my limited testing this wasn't necessary, and the pins themselves were enough to trigger the relays, but overkill is underrated.

5. Put the ReceiverUser creds into the file /var/.awscredentials on the receiver host:
```
[pyropossum-receive]
aws_access_key_id=AKIAXXXXXXXXXXXXXXXX
aws_secret_access_key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```
6. Put the following information into the file /etc/pyropossum/config.json ([here's my config as an example](config/receive-config.json)):
```
{
    "receive-profile":"<the name in brackets in the credentials file>",
    "region":"<AWS region name>",
    "stack":"<CloudFormation stack name>",
    "output":<digital pin on the Arduino to which the device being controlled is connected>
}
```

7. Run the following command to start the pyropossum daemon.  (For some reason it is't currently working with /usr/sbin/service, so you have to directly call the init.d script.)
```
sudo /etc/init.d/pyropossum start
```
If it doesn't appear to be working, logs go to /var/log/pyropossum.log and cron logs go to /var/log/pyropossum.cron

### How to configure an IoT button to be a sender:
1. Still need to write this section, but basically, spin up the iot.cf.json and button.cf.json CloudFormation templates.
