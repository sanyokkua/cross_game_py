from flask import Blueprint, render_template, url_for

INDEX_BLUEPRINT: Blueprint = Blueprint('index_blueprint', __name__, template_folder='templates')


@INDEX_BLUEPRINT.route('/', methods=['GET'])
def _get_index_page() -> str:
    get_new_game_page_url: str = url_for('index_blueprint._get_new_game_page')
    get_join_game_page_url: str = url_for('index_blueprint._get_join_game_page')

    return render_template('index/index_page.html',
                           get_new_game_page_url=get_new_game_page_url,
                           get_join_game_page_url=get_join_game_page_url)


@INDEX_BLUEPRINT.route('/newgame', methods=['GET'])
def _get_new_game_page() -> str:
    post_new_game_url: str = url_for('game_blueprint._post_new_game_redirect_to_wait_for_players_page')

    return render_template('index/new_game_page.html', post_new_game_url=post_new_game_url)


@INDEX_BLUEPRINT.route('/joingame', methods=['GET'])
def _get_join_game_page() -> str:
    post_join_game_url: str = url_for('game_blueprint._post_join_game_redirect_to_game_field_page')

    return render_template('index/join_game_page.html', post_join_game_url=post_join_game_url)
