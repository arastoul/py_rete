from py_rete.common import Token
from py_rete.beta import BetaNode


class PNode(BetaNode):
    """
    A beta network node that stores the matches for productions.
    """

    kind = 'p'

    def __init__(self, children=None, parent=None, items=None, **kwargs):
        """
        :type items: list of Token
        """
        super(PNode, self).__init__(children=children, parent=parent)
        self.items = items if items else []
        self.children = children if children else []
        for k, v in kwargs.items():
            setattr(self, k, v)

    def left_activation(self, token, wme, binding=None):
        """
        :type wme: WME
        :type token: Token
        :type binding: dict
        """
        new_token = Token(token, wme, node=self, binding=binding)
        self.items.append(new_token)

    def execute(self, *args, **kwargs):
        raise NotImplementedError