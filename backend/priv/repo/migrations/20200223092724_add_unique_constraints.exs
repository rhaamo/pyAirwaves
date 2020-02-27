defmodule Pyairwaves.Repo.Migrations.AddUniqueConstraints do
  use Ecto.Migration

  def change do
    create unique_index(:archive_ship, [:mmsi])
    create unique_index(:archive_ship, [:callsign])
    create unique_index(:archive_source, [:name])
  end
end
