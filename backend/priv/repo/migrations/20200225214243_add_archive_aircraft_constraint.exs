defmodule Pyairwaves.Repo.Migrations.AddArchiveAircraftConstraint do
  use Ecto.Migration

  def change do
    create unique_index(:archive_aircraft, [:hex_ident])
  end
end
