# pyropossum

pyropossum is a collection of arduino tools for home automation, currently focused on making it easy to remotely control stuff.  In the future, it may also be expanded to include sensors and data reading.

## Setup
The following terms are used to differentiate the different pieces of the system:

Receiver host: A computer that is waiting to receive instructions by listening on an AWS SQS queue.  It has an Arduino attached over USB to allow it to turn on or off external devices.  (For reference, I'm using a Raspberry Pi Zero Wireless, as it's more than powerful enough and costs $10.)

Sender host: A computer that sends instructions to the AWS SQS queue.  (For reference, I'm just using my laptop.)

### How to set up an Arduino for use with pyropossum:
1. Using the [Arduino IDE](https://www.arduino.cc/en/Main/Software), upload the [arduino.latest.ino](ino/arduino.latest.ino) program to the board.
2. Hook the device you want to control up to one of the digital pins on the Arduino.  Make a note of which pin you use, as you'll need it later.

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
4. Put the following information into the file ~/.pyropossum/config.json:
```
{
    "send-profile":"<the name in brackets in the credentials file>",
    "region":"<AWS region name>",
    "stack":"<CloudFormation stack name>"
}
```
[Here's my config as an example.](config/sender-config.json)

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
1a. If you're using a Raspberry Pi, you can use [PiBakery](http://www.pibakery.org) and [the included recipe](pibakery-recipe.xml) to perform a lot of the setup.  (You'll need to edit it to include your passwords, wifi info, and that sort of thing.)

1b. If you don't want to use PiBakery, you can instead install this from the [receiver-install.sh](install/receiver-install.sh) script.  It has dependencies on python3 and pip3.  Everything after that it should install for you.

2. Put the ReceiverUser creds into the file /var/.awscredentials on the receiver host
```
[pyropossum-receive]
aws_access_key_id=AKIAXXXXXXXXXXXXXXXX
aws_secret_access_key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```
3. Put the following information into the file /etc/pyropossum/config.json:
```
{
    "receive-profile":"<the name in brackets in the credentials file>",
    "region":"<AWS region name>",
    "stack":"<CloudFormation stack name>",
    "output":<digital pin on the Arduino to which the device being controlled is connected>
}
```
[Here's my config as an example.](config/receiver-config.json)

4. Run the following command to start the pyropossum daemon.  (For some reason it is't currently working with /usr/sbin/service, so you have to directly call the init.d script.)
```
/etc/init.d/pyropossum start
```

### How to configure an IoT button to be a sender:
1. Still need to write this section, but basically, spin up the iot.cf.json and button.cf.json CloudFormation templates.
