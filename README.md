# Gremlin Sandbox
## Setting up the project
+ clone it
+ ```mkdir data```
+ ```mkdir data/raw``` -> put the raw data files here
+ ```mkdir data/processed``` -> src/utils will put the processed files there
+ ```mkdir etc; cd etc```
+ ```wget https://www.apache.org/dyn/closer.lua/tinkerpop/3.5.1/apache-tinkerpop-gremlin-console-3.5.1-bin.zip```
+ (If you wanna work locally) ```wget https://www.apache.org/dyn/closer.lua/tinkerpop/3.5.1/apache-tinkerpop-gremlin-server-3.5.1-bin.zip```
+ ```unzip "*.zip"``` (possibly you'll need to use ```chmod``` too)
+ Put your conf file into etc/apache-tinkerpop-gremlin-console-3.x.y/conf:
```yaml
hosts: ["your-neptune-endpoint"]
port: port
serializer: { className: org.apache.tinkerpop.gremlin.driver.ser.GryoMessageSerializerV3d0, config: { serializeResultToString: true }}
```
### AWS credentials
Put your credentials into ```src/creds/awscreds.py``` it must be sth like this
```python
aws_id = "YOUR AWS ID"
aws_secret = "YOUR AWS SECRET"
neptune_endpoint = "ws://yourservicenameandetc:port/gremlin"
test_bucket = "nameofyourbucket"
```

## Headers for node & edge lists
+ vertex `~id	name:String	age:Int	lang:String	interests:String[]	~label`
+ edge `~id	~from	~to	~label	weight:Double`

## Add csv to S3 bucket
Presupposes awscli on your machine.
+ add nodes ```aws s3 cp data/processed/neptune_digest_nodes.csv s3://bucket-name/neptune_digest_nodes.csv```
+ add edges```aws s3 cp data/processed/neptune_digest_edges.csv s3://bucket-name/neptune_digest_edges.csv```

## Work locally
+ Start Gremlin console from etc: ```apache-tinkerpop-gremlin-console-3.5.1/bin/gremlin.sh```
+ Use Neptune services: ```gremlin> :remote connect tinkerpop.server conf/neptune-remote.yaml```
+ If you wanna use it locally, start the Gremlin server before the console. ```./apache-tinkerpop-gremlin-server-3.5.1/bin/gremlin-server.sh start```
+ use local Gremlin server: ```gremlin> :remote connect tinkerpop.server conf/remote.yaml```

# Notes
+ made with vanilla Python 3.8

