defmodule Pyairwaves.Repo.Migrations.AddIndexes do
  use Ecto.Migration

  def change do
    create index(:aircraft, :icao)
  end
end
