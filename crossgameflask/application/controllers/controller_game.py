from flask import (Blueprint, make_response, redirect, render_template,
                   request, url_for)
from werkzeug import Response

import crossgameflask.application.controllers.helpers.form_attributes as attr
from crossgame.logic.game import GameStateDto, WinnerInfo
from crossgameflask.application.configurations.game_config import GAME_CONTROLLER as CONTROLLER
from crossgameflask.application.controllers.helpers.helper_dtos import generate_field
from crossgameflask.application.controllers.helpers.utils import get_str_attr_from_form
from crossgameflask.application.errors.exceptions import NoUserInTheSession

GAME_BLUEPRINT: Blueprint = Blueprint('game_blueprint', __name__, template_folder='templates', url_prefix='/game')


def _render_wait_for_players_page(game_id: str) -> str:
    game_status_page_url: str = url_for('game_blueprint._get_game_status_page', game_id=game_id)
    style_url = url_for('static', filename='custom_game_style.css')

    return render_template('game/wait_for_players_page.html',
                           game_status_page_url=game_status_page_url,
                           game_id=game_id,
                           style_url=style_url)


def _render_finish_game_page(winner_info: WinnerInfo) -> str:
    is_draw: bool = winner_info.is_draw
    sign_name: str = winner_info.sign.name if winner_info.sign is not None else ' '
    player_name: str = winner_info.player.player_name if winner_info.player is not None else ' '
    index_page_url: str = url_for('index_blueprint._get_index_page')

    return render_template('game/finish_game_page.html',
                           is_draw=is_draw,
                           sign_name=sign_name,
                           player_name=player_name,
                           index_page_url=index_page_url)


def _render_game_field_page(game_state: GameStateDto, player_id: str) -> str:
    game_id: str = game_state.game_id
    active_player = game_state.active_player

    is_active_view: bool = active_player.is_active and player_id == active_player.player_id
    get_game_status_page_url: str = url_for('game_blueprint._get_game_status_page', game_id=game_id)
    post_make_move_url: str = url_for('game_blueprint._post_make_move_redirect_to_game_field_page')
    game_field = generate_field(game_state.field)

    players = CONTROLLER.persistance.get_game_info(game_id).players
    player = next((x for x in players if x.player_id == player_id), None)
    pl_name = player.player_name if player is not None else ''
    pl_sign = player.sign.name if player is not None else ''

    style_url = url_for('static', filename='custom_game_style.css')

    return render_template('game/game_field_page.html',
                           game_id=game_id,
                           player_id=player_id,
                           is_active_view=is_active_view,
                           get_game_status_page_url=get_game_status_page_url,
                           post_make_move_url=post_make_move_url,
                           game_field=game_field,
                           style_url=style_url,
                           player_name=pl_name,
                           player_sign=pl_sign)


@GAME_BLUEPRINT.route('/new', methods=['POST'])
def _post_new_game_redirect_to_wait_for_players_page() -> Response:
    player_name: str = get_str_attr_from_form(attr.PLAYER_1_NAME)
    game_state = CONTROLLER.start_game_session(player_name)
    game_id = game_state.game_id

    style_url = url_for('static', filename='custom_game_style.css')

    game_status_page_url: str = url_for('game_blueprint._get_game_status_page', game_id=game_id)
    rendered_template = render_template('game/wait_for_players_page.html',
                                        game_status_page_url=game_status_page_url,
                                        game_id=game_id,
                                        style_url=style_url)

    resp = make_response(rendered_template)
    resp.set_cookie(attr.USER_ID, game_state.active_player.player_id)
    return resp


@GAME_BLUEPRINT.route('/join', methods=['POST'])
def _post_join_game_redirect_to_game_field_page() -> Response:
    player_name: str = get_str_attr_from_form(attr.PLAYER_2_NAME)
    game_id: str = get_str_attr_from_form(attr.GAME_ID)

    game_state = CONTROLLER.join_to_game_game_session(player_name, game_id)
    player = game_state.active_player
    CONTROLLER.start_game(game_id)

    resp = redirect(url_for('game_blueprint._get_game_status_page', game_id=game_id))
    resp.set_cookie(attr.USER_ID, player.player_id)
    return resp


@GAME_BLUEPRINT.route('/move', methods=['POST'])
def _post_make_move_redirect_to_game_field_page() -> Response:
    player_id = request.cookies.get(attr.USER_ID)
    if not player_id:
        raise NoUserInTheSession()
    game_id: str = get_str_attr_from_form(attr.GAME_ID)
    row: int = int(get_str_attr_from_form(attr.ROW))
    column: int = int(get_str_attr_from_form(attr.COLUMN))

    CONTROLLER.make_move(game_id, player_id, row, column)

    return redirect(url_for('game_blueprint._get_game_status_page', game_id=game_id))


@GAME_BLUEPRINT.route('/status/<string:game_id>', methods=['GET'])
def _get_game_status_page(game_id: str) -> str:
    player_id = request.cookies.get(attr.USER_ID)
    if not player_id:
        raise NoUserInTheSession()

    game_state = CONTROLLER.get_status(game_id)

    if game_state is None:
        return _render_wait_for_players_page(game_id)

    if not game_state.is_started:
        return _render_wait_for_players_page(game_id)

    if game_state.winner:
        return _render_finish_game_page(game_state.winner)

    return _render_game_field_page(game_state, player_id)
