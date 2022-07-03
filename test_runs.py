import pytest

from src.classes.schema_root import SchemaRoot
from src.dataclass.import_lol_jsons import ImportLolJsons

json_path: str = "test_jsons"
dtc_path: str = "test_dataclass"
imports = ImportLolJsons(json_path)
sr = SchemaRoot(json_path=json_path, dtc_path=dtc_path)


@pytest.mark.order2
class TestRuns():

    @pytest.fixture
    def jump_line(self):
        yield

    @pytest.mark.usefixtures('jump_line')
    def test_check_jsons(self):
        assert imports.checkJsonsOk() is True

    def do_run(self, name):
        return sr.loadFromJson(name)

    @pytest.mark.usefixtures('jump_line')
    def test_run_versions(self):
        assert self.do_run("versions")

    @pytest.mark.usefixtures('jump_line')
    def test_run_maps(self):
        assert self.do_run("maps")

    @pytest.mark.usefixtures('jump_line')
    def test_run_seasons(self):
        assert self.do_run("seasons")

    @pytest.mark.usefixtures('jump_line')
    def test_run_queues(self):
        assert self.do_run("queues")

    @pytest.mark.usefixtures('jump_line')
    def test_run_gameModes(self):
        assert self.do_run("gameModes")

    @pytest.mark.usefixtures('jump_line')
    def test_run_gameTypes(self):
        assert self.do_run("gameTypes")

    @pytest.mark.usefixtures('jump_line')
    def test_run_regions(self):
        assert self.do_run("regions")

    @pytest.mark.usefixtures('jump_line')
    def test_run_languages(self):
        assert self.do_run("languages")

    @pytest.mark.usefixtures('jump_line')
    def test_run_champions(self):
        assert self.do_run("champions")

    @pytest.mark.usefixtures('jump_line')
    def test_run_summonerSpells(self):
        assert self.do_run("summonerSpells")

    @pytest.mark.usefixtures('jump_line')
    def test_run_profileIcons(self):
        assert self.do_run("profileIcons")

    @pytest.mark.usefixtures('jump_line')
    def test_run_items(self):
        assert self.do_run("items")

    @pytest.mark.usefixtures('jump_line')
    def test_run_featuredMatches(self):
        assert self.do_run("featuredMatches")

    @pytest.mark.usefixtures('jump_line')
    def test_run_summoner(self):
        assert self.do_run("summoner")

    @pytest.mark.usefixtures('jump_line')
    def test_run_spectator(self):
        assert self.do_run("spectator")

    @pytest.mark.usefixtures('jump_line')
    def test_run_matches(self):
        assert self.do_run("matches")

    @pytest.mark.usefixtures('jump_line')
    def test_run_match(self):
        assert self.do_run("match")

    @pytest.mark.usefixtures('jump_line')
    def test_run_matchTimeline(self):
        assert self.do_run("matchTimeline")

    @pytest.mark.usefixtures('jump_line')
    def test_run_challenges(self):
        assert self.do_run("challenges")

    @pytest.mark.usefixtures('jump_line')
    def test_run_championsMasteries(self):
        assert self.do_run("championsMasteries")
