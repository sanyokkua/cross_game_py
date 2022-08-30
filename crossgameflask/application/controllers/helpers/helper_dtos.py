from dataclasses import dataclass

from crossgame.logic.game_enums import Sign


@dataclass
class ViewFieldCell:
    row: int
    col: int
    value: str = ' '


def generate_field(field: list[list[Sign]]) -> list[list[ViewFieldCell]]:
    rows: list[list[ViewFieldCell]] = []
    for row, row_val in enumerate(field):
        column: list[ViewFieldCell] = []
        for col, col_val in enumerate(row_val):
            val = col_val.name if col_val is not None else ' '
            column.append(ViewFieldCell(row, col, val))
        rows.append(column)
    return rows
