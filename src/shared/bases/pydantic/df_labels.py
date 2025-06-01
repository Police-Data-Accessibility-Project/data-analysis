from dataclasses import dataclass, fields, is_dataclass


@dataclass(frozen=True)
class DataFrameLabelsBase:

    def as_list(self) -> list[str]:
        return list(self._flatten_values().values())

    def as_dict(self) -> dict[str, str]:
        return self._flatten_values()

    def has_label(self, label: str) -> bool:
        return label in self.as_list()

    def has_field(self, name: str) -> bool:
        return hasattr(self, name)

    def _flatten_values(self) -> dict[str, str]:
        """
        Flatten nested labels (for label classes with label class attributes).
        :return:
        """

        result = {}
        for f in fields(self):
            val = getattr(self, f.name)
            if is_dataclass(val) and isinstance(val, DataFrameLabelsBase):
                nested = val._flatten_values()
                result.update(nested)
            else:
                result[f.name] = val
        return result