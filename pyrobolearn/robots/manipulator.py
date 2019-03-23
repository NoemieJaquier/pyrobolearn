#!/usr/bin/env python
"""Provide the manipulator abstract classes.
"""

from pyrobolearn.robots.robot import Robot


class ManipulatorRobot(Robot):
    r"""Manipulator robot

    Manipulator robots are robots that use some of its end-effectors to manipulate objects in its environment.
    """

    def __init__(self,
                 simulator,
                 urdf,
                 position=(0, 0, 0.),
                 orientation=(0, 0, 0, 1),
                 fixed_base=False,
                 scaling=1.):
        super(ManipulatorRobot, self).__init__(simulator, urdf, position, orientation, fixed_base, scaling)

        self.arms = []  # list of arms where an arm is a list of links
        self.hands = []  # list of end-effectors/hands

    ##############
    # Properties #
    ##############

    @property
    def num_arms(self):
        """Return the number of arms"""
        return len(self.arms)

    @property
    def num_hands(self):
        """Return the number of hands; this is normally equal to the number of arms"""
        return len(self.hands)

    ###########
    # Methods #
    ###########

    def get_arm_ids(self, arms=None):
        """
        Return the arm's link id(s) from the name(s) or index(ices).

        Args:
            arms (str, int, list of str/int, None): if str, it will get the arm's link id associated to the given
                name. If int, it will get the arm's link id associated to the given index. If it is a list of str
                and/or int, it will get the corresponding arm's link ids. If None, it will return all the arm's
                link ids.

        Returns:
            if 1 arm's link:
                int: link id
            if multiple arm's links:
                int[N]: link ids
        """
        if arms is not None:
            if isinstance(arms, int):
                return self.arms[arms]
            elif isinstance(arms, str):
                return self.arms[self.get_link_ids(arms)]
            elif isinstance(arms, (list, tuple)):
                arm_ids = []
                for arm in arms:
                    if isinstance(arm, int):
                        arm_ids.append(self.arms[arm])
                    elif isinstance(arm, str):
                        arm_ids.append(self.arms[self.get_link_ids(arm)])
                    else:
                        raise TypeError("Expecting a str or int for items in arms")
                return arm_ids
        return self.arms

    def get_hand_ids(self, hands=None):
        """
        Return the hand's link id(s) from the name(s) or index(ices).

        Args:
            hands (str, int, list of str/int, None): if str, it will get the hand's link id associated to the given
                name. If int, it will get the hand's link id associated to the given index. If it is a list of str
                and/or int, it will get the corresponding hand's link ids. If None, it will return all the hand's
                link ids.

        Returns:
            if 1 hand's link:
                int: link id
            if multiple hand's links:
                int[N]: link ids
        """
        if hands is not None:
            if isinstance(hands, int):
                return self.hands[hands]
            elif isinstance(hands, str):
                return self.hands[self.get_link_ids(hands)]
            elif isinstance(hands, (list, tuple)):
                hand_ids = []
                for hand in hands:
                    if isinstance(hand, int):
                        hand_ids.append(self.hands[hand])
                    elif isinstance(hand, str):
                        hand_ids.append(self.hands[self.get_link_ids(hand)])
                    else:
                        raise TypeError("Expecting a str or int for items in hands")
                return hand_ids
        return self.hands


class BiManipulatorRobot(ManipulatorRobot):
    r"""Bi-manipulator Robot

    Bi-manipulators are robots that have two manipulators to manipulate objects in the environment.
    """

    def __init__(self, simulator, urdf, position=(0, 0, 1.5), orientation=(0, 0, 0, 1), fixed_base=False,
                 scaling=1.):
        super(BiManipulatorRobot, self).__init__(simulator, urdf, position, orientation, fixed_base, scaling)

        self.left_arm_id = 0
        self.left_hand_id = 0
        self.right_arm_id = 1
        self.right_hand_id = 1

    ##############
    # Properties #
    ##############

    @property
    def left_arm(self):
        return self.arms[self.left_arm_id]

    @property
    def right_arm(self):
        return self.arms[self.right_arm_id]

    @property
    def left_hand(self):
        return self.hands[self.left_hand_id]

    @property
    def right_hand(self):
        return self.hands[self.right_arm_id]
