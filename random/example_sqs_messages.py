#!/usr/bin/env python3

test_singleclick = {
    "MessageId": "020efce0-38d6-4dc3-9552-e09317d168bf",
    "ReceiptHandle": "AQEBDfngYj7g4kfpu7sRRK/onRKEJC0H/Y9d8Lqmh+zlubt+GfT4QEUzOhfmlSBDBUxj7C/juaAkwJsIHhqSGbxL4hTswJd2MN3otjjUc5sWXfrZ+yg+2OS73S5S7odyCC1yrST4MQ/+pQf1VtK/o0zazfeUN05X7kcNV9q+odli3SZlk7UkIM8O4QSC7Y6yf05DANTshMzdK87IJMR2j+P3Z+kynkrgnCnVQGbCRTD0C/57YuNk2jf0niSV/uHMUHRrmHYCWlkDZGQkhWeHjSYIH0AfZy8UmBw6hd4Hj6tYs94xbHSaYIV0oIhhm3TSU/5jXEXGSvN9LXYeQaRKL+wK1W20W3Ef4pO7tE4JK2Zlpk67YaDy6vU22WHfbKsh8eGUPqlRzCiACx2+qIgVDWXMEA==",
    "MD5OfBody": "c6ce8b96dfaef32d5b99a367548ad729",
    "Body": "{\n  \"Type\" : \"Notification\",\n  \"MessageId\" : \"9ad85a83-3683-5e56-b97c-0b65cc33a342\",\n  \"TopicArn\" : \"arn:aws:sns:us-east-1:856133803657:aws-iot-button-sns-topic\",\n  \"Message\" : \"{\\\"serialNumber\\\": \\\"G030MD027312N5RN\\\", \\\"batteryVoltage\\\": \\\"1701mV\\\", \\\"clickType\\\": \\\"SINGLE\\\"}\",\n  \"Timestamp\" : \"2017-07-17T17:48:32.076Z\",\n  \"SignatureVersion\" : \"1\",\n  \"Signature\" : \"Kr1nnyrd5z5QVQVPAPS0rrKHZClI5yzXznDHdY1/RKIs62GtGf1NbZ/ADDdbgVRGEEO1Z2mt2rtj6lYfEiBPovlRJE5WBc43LjL/Q6JljOH5rFrAKy7c/dsTDOVnDfwyUk8vPqx4vENOAA/uCbMHVw2bTh4dravZpKdUOgfKeY9CIUSSvkr1wr0pQqpZdHimD3TAN1ExiezcjqdCI5N1+ye1JUK3iJKio7FDWA/upXSWvMwftwZ8gFAVNPeqr4dtVsuATZ7EmiHCRtATkBxT7nS7qjKyMNWvkigD6kThbalRXKhYKAMwDHxtHsTpVMhvQ0xCo4JCjvcGu+u5zN25WQ==\",\n  \"SigningCertURL\" : \"https://sns.us-east-1.amazonaws.com/SimpleNotificationService-b95095beb82e8f6a046b3aafc7f4149a.pem\",\n  \"UnsubscribeURL\" : \"https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:856133803657:aws-iot-button-sns-topic:84332d3c-1453-495e-93fc-df723d3ecbaa\"\n}",
    "Attributes": {
        "SenderId": "AIDAIT2UOQQY3AUEKVGXU",
        "ApproximateFirstReceiveTimestamp": "1500313712124",
        "ApproximateReceiveCount": "5",
        "SentTimestamp": "1500313712124"
    }
}

test_doubleclick = {
    "MessageId": "020efce0-38d6-4dc3-9552-e09317d168bf",
    "ReceiptHandle": "AQEBDfngYj7g4kfpu7sRRK/onRKEJC0H/Y9d8Lqmh+zlubt+GfT4QEUzOhfmlSBDBUxj7C/juaAkwJsIHhqSGbxL4hTswJd2MN3otjjUc5sWXfrZ+yg+2OS73S5S7odyCC1yrST4MQ/+pQf1VtK/o0zazfeUN05X7kcNV9q+odli3SZlk7UkIM8O4QSC7Y6yf05DANTshMzdK87IJMR2j+P3Z+kynkrgnCnVQGbCRTD0C/57YuNk2jf0niSV/uHMUHRrmHYCWlkDZGQkhWeHjSYIH0AfZy8UmBw6hd4Hj6tYs94xbHSaYIV0oIhhm3TSU/5jXEXGSvN9LXYeQaRKL+wK1W20W3Ef4pO7tE4JK2Zlpk67YaDy6vU22WHfbKsh8eGUPqlRzCiACx2+qIgVDWXMEA==",
    "MD5OfBody": "c6ce8b96dfaef32d5b99a367548ad729",
    "Body": "{\n  \"Type\" : \"Notification\",\n  \"MessageId\" : \"9ad85a83-3683-5e56-b97c-0b65cc33a342\",\n  \"TopicArn\" : \"arn:aws:sns:us-east-1:856133803657:aws-iot-button-sns-topic\",\n  \"Message\" : \"{\\\"serialNumber\\\": \\\"G030MD027312N5RN\\\", \\\"batteryVoltage\\\": \\\"1701mV\\\", \\\"clickType\\\": \\\"DOUBLE\\\"}\",\n  \"Timestamp\" : \"2017-07-17T17:48:32.076Z\",\n  \"SignatureVersion\" : \"1\",\n  \"Signature\" : \"Kr1nnyrd5z5QVQVPAPS0rrKHZClI5yzXznDHdY1/RKIs62GtGf1NbZ/ADDdbgVRGEEO1Z2mt2rtj6lYfEiBPovlRJE5WBc43LjL/Q6JljOH5rFrAKy7c/dsTDOVnDfwyUk8vPqx4vENOAA/uCbMHVw2bTh4dravZpKdUOgfKeY9CIUSSvkr1wr0pQqpZdHimD3TAN1ExiezcjqdCI5N1+ye1JUK3iJKio7FDWA/upXSWvMwftwZ8gFAVNPeqr4dtVsuATZ7EmiHCRtATkBxT7nS7qjKyMNWvkigD6kThbalRXKhYKAMwDHxtHsTpVMhvQ0xCo4JCjvcGu+u5zN25WQ==\",\n  \"SigningCertURL\" : \"https://sns.us-east-1.amazonaws.com/SimpleNotificationService-b95095beb82e8f6a046b3aafc7f4149a.pem\",\n  \"UnsubscribeURL\" : \"https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:856133803657:aws-iot-button-sns-topic:84332d3c-1453-495e-93fc-df723d3ecbaa\"\n}",
    "Attributes": {
        "SenderId": "AIDAIT2UOQQY3AUEKVGXU",
        "ApproximateFirstReceiveTimestamp": "1500313712124",
        "ApproximateReceiveCount": "5",
        "SentTimestamp": "1500313712124"
    }
}
