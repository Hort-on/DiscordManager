from dataclasses import dataclass


@dataclass
class AvailableUsers:
    available_users: dict[int, str]
    not_found_ids: set[int]


@dataclass
class AddSuperusersResult:
    added_ids: set[int]
    added_names: set[str]
    not_found: set[str]
    already_super: set[str]


@dataclass
class DeleteSuperusersResult:
    deleted: set[str]
    not_found_message: str | None


@dataclass
class ResolvedUsers:
    added_ids: list[int]
    added_names: list[str]
    not_found: list[str]
    already_super: list[str]
