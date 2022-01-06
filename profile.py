"""An example of constructing a profile that requests a specific raw PC. It
can be instantiated only on the cluster where that pc is located; the node will boot the default operating system, which is typically a recent version of Ubuntu.

Instructions:
Wait for the profile instance to start, then click on the node in the topology and choose the `shell` menu item. 
"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg

# We use the URN library below.
import geni.urn as urn
# Emulab extension
import geni.rspec.emulab

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Define a parameter to set the node. Needs to be a URN.
pc.defineParameter("NodeID", "Node URN",
                   portal.ParameterType.STRING, 
                   "urn:publicid:IDN+emulab.net+node+pc444")
params = pc.bindParameters()

if params.NodeID == '':
    perr = portal.ParameterError("Must provide a node URN!", ['NodeID'])
    pc.reportError(perr, immediate=True)
    pass
if not urn.Base.isValidURN(params.NodeID):
    perr = portal.ParameterError("Not a valid node URN!", ['NodeID'])
    pc.reportError(perr, immediate=True)
    pass
 
# Add a raw PC to the request.
node = request.RawPC("node1")
# Assign to a node on emulab.net
node.component_id = params.NodeID
# Use the default image for the type of the node selected. 
node.b210_node_disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU18-64-STD"

node.addService(pg.Execute(shell="bash", command="/local/repository/startup.sh"))

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)