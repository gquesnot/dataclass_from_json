import pytest

from src.controllers.schema_root import SchemaRoot
from src.dataclass.import_lol_jsons import ImportLolJsons

json_path: str = "test_jsons"
dtc_path: str = "test_dataclass"
imports = ImportLolJsons(json_path)
sr = SchemaRoot(json_path=json_path, dtc_path=dtc_path)


@pytest.mark.order1
class TestBuild():

    @pytest.fixture
    def jump_line(self):
        yield
        print('\n')

    @pytest.mark.usefixtures('jump_line')
    def test_check_jsons(self):
        assert imports.checkJsonsOk() is True

    def do_build(self, name):
        sr.generate(name)
        return True

    @pytest.mark.usefixtures('jump_line')
    def test_build_versions(self):
        assert self.do_build("versions")

    @pytest.mark.usefixtures('jump_line')
    def test_build_maps(self):
        assert self.do_build("maps")

    @pytest.mark.usefixtures('jump_line')
    def test_build_seasons(self):
        assert self.do_build("seasons")

    @pytest.mark.usefixtures('jump_line')
    def test_build_queues(self):
        assert self.do_build("queues")

    @pytest.mark.usefixtures('jump_line')
    def test_build_gameModes(self):
        assert self.do_build("gameModes")

    @pytest.mark.usefixtures('jump_line')
    def test_build_gameTypes(self):
        assert self.do_build("gameTypes")

    @pytest.mark.usefixtures('jump_line')
    def test_build_regions(self):
        assert self.do_build("regions")

    @pytest.mark.usefixtures('jump_line')
    def test_build_languages(self):
        assert self.do_build("languages")

    @pytest.mark.usefixtures('jump_line')
    def test_build_champions(self):
        assert self.do_build("champions")

    @pytest.mark.usefixtures('jump_line')
    def test_build_summonerSpells(self):
        assert self.do_build("summonerSpells")

    @pytest.mark.usefixtures('jump_line')
    def test_build_profileIcons(self):
        assert self.do_build("profileIcons")

    @pytest.mark.usefixtures('jump_line')
    def test_build_items(self):
        assert self.do_build("items")

    @pytest.mark.usefixtures('jump_line')
    def test_build_featuredMatches(self):
        assert self.do_build("featuredMatches")

    @pytest.mark.usefixtures('jump_line')
    def test_build_summoner(self):
        assert self.do_build("summoner")

    @pytest.mark.usefixtures('jump_line')
    def test_build_spectator(self):
        assert self.do_build("spectator")

    @pytest.mark.usefixtures('jump_line')
    def test_build_matches(self):
        assert self.do_build("matches")

    @pytest.mark.usefixtures('jump_line')
    def test_build_match(self):
        assert self.do_build("match")

    @pytest.mark.usefixtures('jump_line')
    def test_build_matchTimeline(self):
        assert self.do_build("matchTimeline")

    @pytest.mark.usefixtures('jump_line')
    def test_build_challenges(self):
        assert self.do_build("challenges")

    @pytest.mark.usefixtures('jump_line')
    def test_build_championsMasteries(self):
        assert self.do_build("championsMasteries")
