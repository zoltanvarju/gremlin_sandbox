import boto3
from gremlin_python.driver import client as gclient

from src.creds.awscreds import aws_id, aws_secret, neptune_endpoint, test_bucket
from src.utils.csv_gremlin import NeptuneCSVReader

###############################################################################
#####                                  Setup                              #####
###############################################################################
# connect for scripting
gremlin_client = gclient.Client(
    neptune_endpoint,
    "g",
)

gremlin_client.submit("graph = TinkerGraph.open()")

gremlin_client.submit("g = traversal().withEmbedded(graph)")

##TODO: combine it with load_data
client = boto3.client("s3", aws_access_key_id=aws_id, aws_secret_access_key=aws_secret)

bucket_name = test_bucket

nodes_object_key = "neptune_digest_nodes.csv"
nodes_csv_obj = client.get_object(Bucket=bucket_name, Key=nodes_object_key)
nodes_body = nodes_csv_obj["Body"]
nodes_csv_string = nodes_body.read().decode("utf-8")

edges_object_key = "neptune_digest_edges.csv"
edges_csv_obj = client.get_object(Bucket=bucket_name, Key=edges_object_key)
edges_body = edges_csv_obj["Body"]
edges_csv_string = edges_body.read().decode("utf-8")


###############################################################################
#####                               Loader                                #####
###############################################################################
def load_data(csv):
    """Loads a properly formatted csv into g
    csv can be node list or edge list or even a mixed list
    """
    ncsv = NeptuneCSVReader(silent_mode=True)
    ncsv.set_batch_sizes(vbatch=100, ebatch=100)
    ncsv.set_max_rows(100000000000000)
    ncsv.process_csv_file(csv)
    for b in ncsv.batches:
        gremlin_client.submit(b)
# ###############################################################################
# #####                            Sandbox                                  #####
# ###############################################################################
load_data(nodes_csv_string)
load_data(edges_csv_string)
