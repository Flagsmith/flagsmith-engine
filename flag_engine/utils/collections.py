from collections import UserList

from flag_engine.features.models import FeatureStateModel
from flag_engine.utils.exceptions import DuplicateFeatureState


class IdentityFeaturesList(UserList):
    def append(self, feature_state: FeatureStateModel):
        if [fs for fs in self.data if fs.feature.id == feature_state.feature.id]:
            raise DuplicateFeatureState("feature state for this feature already exists")

        super().append(feature_state)
