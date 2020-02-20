defmodule Pyairwaves.Repo.Migrations.CreateAircraftMode do
  use Ecto.Migration

  def change do
    create_if_not_exists table(:aircraft_mode) do
      add :icao_type_code, :string, size: 4
      add :mode_s, :string, size: 6
      add :mode_s_country, :string, size: 40
      add :registration, :string, size: 20
      add :source, :string, size: 255
      add :source_type, :string, size: 255, default: "modes"
      add :type_flight, :string, size: 50

      timestamps()
    end

    create index(:aircraft_mode, :mode_s)
    create index(:aircraft_mode, :mode_s_country)
    create index(:aircraft_mode, :registration)
    create index(:aircraft_mode, :icao_type_code)

  end
end
