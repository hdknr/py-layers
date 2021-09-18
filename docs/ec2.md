# ec2

## Instance

- Instance ID, Name, Public IP

~~~bash
% jq -r ".[] |[.InstanceId, .Tags[0].Value, .NetworkInterfaces[0].Association.PublicIp, .ImageId] | @csv"
~~~


## Image

~~~bash
% jq -r ".[]|[.ImageId, .State, .Name, .Tags[0].Value]|@csv"
~~~