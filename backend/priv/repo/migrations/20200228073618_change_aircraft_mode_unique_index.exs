defmodule Pyairwaves.Repo.Migrations.ChangeAircraftModeUniqueIndex do
  use Ecto.Migration

  def up do
    IO.puts("!!! Please re-run the mix task 'pyairwaves.update_aircrafts_mode_s' after the migrations ended.")
    drop index(:aircraft_mode, :mode_s)
    statement = """
    DELETE
      FROM
        aircraft_mode T1
      USING
        aircraft_mode T2
    WHERE
      T1.mode_s = T2.mode_s
    """
    execute(statement)
    create unique_index(:aircraft_mode, [:mode_s])
  end

  def up do
    drop unique_index(:aircraft_mode, [:mode_s])
    create index(:aircraft_mode, :mode_s)
  end
end
