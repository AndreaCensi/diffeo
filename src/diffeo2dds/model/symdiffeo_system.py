from contracts import contract

class SymDiffeoSystem(object):
    """ This is an idealized description of a diffeo system. """
    
    @contract(topology=str, actions='list(dict)')
    def __init__(self, topology, actions):
        self.actions = actions
        self.topology = topology


#         
# 
# - id: dcl1
#   desc: |
#     Car-like robot 
#   code:
#   - diffeo2dds.DDSFromSymbolic
#   - resolution: 128
#     actions:  # vel, steering
#     - original_cmd: [1, 0] # forward 
#       diffeo: pX10
#       label: fwd
#     - original_cmd: [1, 1] # forward, right
#       diffeo: [pX10, pR10]
#       label: fwdR
#     - original_cmd: [1, -1] # forward 
#       diffeo: [pX10, IpR10]
#       label: fwdL
#     - original_cmd: [-1, 0] # forward 
#       diffeo: IpX10
#       label: bck
#     - original_cmd: [-1, 1] # forward, right
#       diffeo: [IpX10, pR10]
#       label: bckR
#     - original_cmd: [-1, -1] # forward 
#       diffeo: [IpX10, IpR10]
#       label: bckL
#     topology: plane
