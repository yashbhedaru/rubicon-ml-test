from dash import Dash

from rubicon_ml.viz import ExperimentsTable


def test_experiments_table(viz_experiments):
    experiments_table = ExperimentsTable(experiments=viz_experiments, is_selectable=True)

    expected_experiment_ids = [e.id for e in viz_experiments]

    for experiment in experiments_table.experiments:
        assert experiment.id in expected_experiment_ids

        expected_experiment_ids.remove(experiment.id)

    assert len(expected_experiment_ids) == 0
    assert experiments_table.is_selectable is True


def test_experiments_table_load_data(viz_experiments):
    experiments_table = ExperimentsTable(experiments=viz_experiments)
    experiments_table.load_experiment_data()

    expected_experiment_ids = [e.id for e in viz_experiments]
    expected_metric_names = [m.name for m in viz_experiments[0].metrics()]
    expected_parameter_names = [p.name for p in viz_experiments[0].parameters()]

    for record in experiments_table.experiment_records:
        assert record["id"] in expected_experiment_ids
        assert all([record.get(name) is not None for name in expected_metric_names])
        assert all([record.get(name) is not None for name in expected_parameter_names])

    assert experiments_table.commit_hash == viz_experiments[0].commit_hash
    assert experiments_table.github_url == f"test.github.url/tree/{viz_experiments[0].commit_hash}"


def test_experiments_table_layout(viz_experiments):
    experiments_table = ExperimentsTable(experiments=viz_experiments)
    experiments_table.load_experiment_data()
    layout = experiments_table.layout

    assert len(layout.children) == 2
    assert layout.children[-1].children.id == "experiment-table"


def test_experiments_table_layout_selectable(viz_experiments):
    experiments_table = ExperimentsTable(experiments=viz_experiments, is_selectable=True)
    experiments_table.load_experiment_data()
    layout = experiments_table.layout

    assert len(layout.children) == 3
    assert layout.children[-1].children.id == "experiment-table"


def test_experiments_table_register_callbacks(viz_experiments):
    experiments_table = ExperimentsTable(experiments=viz_experiments)
    experiments_table.app = Dash(__name__, title="test callbacks")
    experiments_table.register_callbacks()

    callback_values = list(experiments_table.app.callback_map.values())

    assert len(callback_values) == 3

    registered_callback_names = [callback["callback"].__name__ for callback in callback_values]

    assert "update_selected_column_checkboxes" in registered_callback_names
    assert "update_hidden_experiment_table_cols" in registered_callback_names
    assert "update_selected_experiment_table_rows" in registered_callback_names
