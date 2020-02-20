defmodule Pyairwaves.Repo.Migrations.CreateAircraftRegistration do
  use Ecto.Migration

  def change do
    create_if_not_exists table(:aircraft_registration) do
      add :country, :string
      add :prefix, :string
    end

    create index(:aircraft_registration, :country)

  end
end
