defmodule Pyairwaves.Repo.Migrations.DropUnusedIndex do
  use Ecto.Migration

  def change do
    drop index(:aircraft_registration, :country)
  end
end
